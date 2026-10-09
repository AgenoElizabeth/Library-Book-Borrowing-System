import pytest

from src.domain.book_items.value_objects.ISBN import ISBN


@pytest.mark.coursework
def test_t1_isbn_value_rule_accepts_valid_and_rejects_invalid_values() -> None:
    # T1 - BR1: valid ISBN-13 values are accepted and invalid ones rejected.
    valid_isbn = ISBN.create("978-0132350884")
    assert valid_isbn.value == "9780132350884"

    with pytest.raises(ValueError) as exception_info:
        ISBN.create("978-0132350885")

    assert "The ISBN check digit is not valid" in str(exception_info.value)
