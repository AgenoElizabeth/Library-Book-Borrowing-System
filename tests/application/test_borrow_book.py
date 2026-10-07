from copy import deepcopy
from datetime import date

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