from datetime import date

import pytest

from src.domain.borrower_accounts.BorrowerAccount import BorrowerAccount
from src.domain.borrower_accounts.value_objects.BorrowerType import BorrowerType


@pytest.mark.coursework
def test_t3_borrower_limit_invariant_allows_reaching_the_limit() -> None:
    # T3 - BR3 (boundary): the final borrowing that reaches the limit is accepted.
    # Arrange
    account = BorrowerAccount("ST123", BorrowerType.STUDENT, borrowing_limit=5)
    for number in range(1, 5):
        account.record_borrowing(f"BI00{number}", date(2026, 10, 1), date(2026, 10, 15))

    # Act
    account.record_borrowing("BI005", date(2026, 10, 1), date(2026, 10, 15))

    # Assert
    assert len(account.active_borrowings) == 5
