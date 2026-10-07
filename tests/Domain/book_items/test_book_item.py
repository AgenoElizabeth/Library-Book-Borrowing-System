from datetime import date

import pytest

from src.domain.book_items.BookItem import BookItem
from src.domain.book_items.value_objects.BookItemStatus import BookItemStatus
from src.domain.book_items.value_objects.ISBN import ISBN


def available_book_item() -> BookItem:
    return BookItem("BI001", ISBN("978-0132350884"))
    