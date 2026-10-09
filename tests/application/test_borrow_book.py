from copy import deepcopy
from datetime import date

import pytest

from src.application.borrowing.BookBorrowedHandler import BookBorrowedHandler
from src.application.borrowing.BorrowBookApplicationService import (
    BorrowBookApplicationService,
)
from src.application.borrowing.BorrowBookInputDTO import BorrowBookInputDTO
from src.domain.book_items.BookItem import BookItem
from src.domain.book_items.events.BookBorrowed import BookBorrowed
from src.domain.book_items.repositories.BookItemRepository import BookItemRepository
from src.domain.book_items.value_objects.BookItemStatus import BookItemStatus
from src.domain.book_items.value_objects.ISBN import ISBN
from src.domain.borrower_accounts.BorrowerAccount import BorrowerAccount
from src.domain.borrower_accounts.repositories.BorrowerAccountRepository import (
    BorrowerAccountRepository,
)
from src.domain.borrower_accounts.services.LoanDueDateService import LoanDueDateService
from src.domain.borrower_accounts.value_objects.BorrowerType import BorrowerType


# Test doubles live in the test suite, so application tests do not depend on
# concrete infrastructure adapters. They follow the repository contract:
# find_by_id returns a copy, and only save changes what is stored.
class FakeBookItemRepository(BookItemRepository):
    def __init__(self, *book_items: BookItem) -> None:
        self._book_items = {item.id: deepcopy(item) for item in book_items}

    def find_by_id(self, book_item_id: str) -> BookItem | None:
        return deepcopy(self._book_items.get(book_item_id))

    def save(self, book_item: BookItem) -> None:
        self._book_items[book_item.id] = deepcopy(book_item)


class FakeBorrowerAccountRepository(BorrowerAccountRepository):
    def __init__(self, *accounts: BorrowerAccount) -> None:
        self._accounts = {account.id: deepcopy(account) for account in accounts}

    def find_by_id(self, student_id: str) -> BorrowerAccount | None:
        return deepcopy(self._accounts.get(student_id))

    def save(self, account: BorrowerAccount) -> None:
        self._accounts[account.id] = deepcopy(account)


class RecordingBookBorrowedHandler(BookBorrowedHandler):
    """The real handler, which also remembers the events it received."""

    def __init__(self, borrower_accounts: BorrowerAccountRepository) -> None:
        super().__init__(borrower_accounts)
        self.received_events: list[BookBorrowed] = []

    def handle(self, event: BookBorrowed) -> None:
        self.received_events.append(event)
        super().handle(event)


TODAY = date(2026, 10, 1)


def borrower_with_active_borrowings(limit: int, active: int) -> BorrowerAccount:
    account = BorrowerAccount("ST123", BorrowerType.STUDENT, borrowing_limit=limit)
    for number in range(active):
        account.record_borrowing(f"OLD{number}", TODAY, date(2026, 10, 15))
    return account


@pytest.mark.coursework
def test_t5_book_borrowed_event_requests_borrower_account_follow_up() -> None:
    # T5 - BR5: handling BookBorrowed asks Aggregate B to record the borrowing.
    borrower_accounts = FakeBorrowerAccountRepository(
        borrower_with_active_borrowings(limit=3, active=0)
    )
    handler = BookBorrowedHandler(borrower_accounts)
    event = BookBorrowed("BI001", "ST123", TODAY, date(2026, 10, 15))

    handler.handle(event)

    recorded = borrower_accounts.find_by_id("ST123").active_borrowings
    assert [(borrowing.book_item_id, borrowing.due_date) for borrowing in recorded] == [
        ("BI001", date(2026, 10, 15))
    ]


@pytest.mark.coursework
def test_t6_borrowing_continues_after_finding_the_book_item() -> None:
    # T6 - BR6: the repository finds the existing BookItem and the use case proceeds.
    book_items = FakeBookItemRepository(BookItem("BI001", ISBN("978-0132350884")))
    borrower_accounts = FakeBorrowerAccountRepository(
        borrower_with_active_borrowings(limit=3, active=0)
    )
    handler = RecordingBookBorrowedHandler(borrower_accounts)
    borrow_book = BorrowBookApplicationService(
        book_items, borrower_accounts, LoanDueDateService(), handler, today=lambda: TODAY
    )

    result = borrow_book.execute(BorrowBookInputDTO("ST123", "BI001"))

    assert result.success
    assert book_items.find_by_id("BI001").status is BookItemStatus.BORROWED
    assert borrower_accounts.find_by_id("ST123").active_borrowings[0].book_item_id == "BI001"
    assert [event.book_item_id for event in handler.received_events] == ["BI001"]


@pytest.mark.coursework
def test_t7_borrowing_a_book_records_the_borrowing_through_the_event() -> None:
    # T7 - BR5/BR6: the main use case succeeds and BookBorrowed is handled.
    # Arrange
    book_items = FakeBookItemRepository(BookItem("BI001", ISBN("978-0132350884")))
    borrower_accounts = FakeBorrowerAccountRepository(
        borrower_with_active_borrowings(limit=3, active=0)
    )
    handler = RecordingBookBorrowedHandler(borrower_accounts)
    borrow_book = BorrowBookApplicationService(
        book_items, borrower_accounts, LoanDueDateService(), handler, today=lambda: TODAY
    )

    # Act
    result = borrow_book.execute(BorrowBookInputDTO("ST123", "BI001"))

    # Assert
    assert result.success
    assert result.due_date == date(2026, 10, 15)
    assert book_items.find_by_id("BI001").status is BookItemStatus.BORROWED
    assert [event.book_item_id for event in handler.received_events] == ["BI001"]
    recorded = borrower_accounts.find_by_id("ST123").active_borrowings
    assert [borrowing.book_item_id for borrowing in recorded] == ["BI001"]


@pytest.mark.coursework
def test_t8_the_borrower_account_rejects_the_follow_up_at_its_limit() -> None:
    # T8 - BR3/BR5 (rejection): Aggregate B rejects the follow-up action and
    # the final state stays consistent.
    # Arrange
    book_items = FakeBookItemRepository(BookItem("BI001", ISBN("978-0132350884")))
    borrower_accounts = FakeBorrowerAccountRepository(
        borrower_with_active_borrowings(limit=5, active=5)
    )
    handler = RecordingBookBorrowedHandler(borrower_accounts)
    borrow_book = BorrowBookApplicationService(
        book_items, borrower_accounts, LoanDueDateService(), handler, today=lambda: TODAY
    )

    # Act
    result = borrow_book.execute(BorrowBookInputDTO("ST123", "BI001"))

    # Assert
    assert not result.success
    assert "has reached the borrowing limit of 5" in result.message
    assert len(handler.received_events) == 1
    assert len(borrower_accounts.find_by_id("ST123").active_borrowings) == 5
    assert book_items.find_by_id("BI001").status is BookItemStatus.AVAILABLE
