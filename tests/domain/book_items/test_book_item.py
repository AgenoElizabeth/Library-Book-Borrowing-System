from datetime import date

import pytest

from src.domain.book_items.BookItem import BookItem
from src.domain.book_items.value_objects.BookItemStatus import BookItemStatus
from src.domain.book_items.value_objects.ISBN import ISBN


def available_book_item() -> BookItem:
    return BookItem("BI001", ISBN("978-0132350884"))


@pytest.mark.coursework
def test_t2_book_item_state_rule_allows_only_available_items_to_be_borrowed() -> None:
    # T2 - BR2: an AVAILABLE BookItem can be borrowed; a BORROWED one cannot.
    book_item = available_book_item()

    book_item.borrow("ST123", date(2026, 10, 1), date(2026, 10, 15))
    assert book_item.status is BookItemStatus.BORROWED

    with pytest.raises(ValueError) as exception_info:
        book_item.borrow("ST456", date(2026, 10, 2), date(2026, 10, 16))

    assert "BookItem BI001 is already borrowed" in str(exception_info.value)
    assert book_item.status is BookItemStatus.BORROWED
