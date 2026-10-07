import pytest

from src.domain.book_items.value_objects.ISBN import ISBN


def test_t1_a_valid_isbn_is_accepted() -> None:
    # T1 - BR1: a valid ISBN-13 is accepted.
    # Arrange
    value = "978-0132350884"

    # Act
    isbn = ISBN.create(value)

    # Assert
    assert isbn.value == "9780132350884"