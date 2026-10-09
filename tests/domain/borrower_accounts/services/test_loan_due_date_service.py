from datetime import date

import pytest

from src.domain.borrower_accounts.services.LoanDueDateService import LoanDueDateService
from src.domain.borrower_accounts.value_objects.BorrowerType import BorrowerType


@pytest.mark.coursework
def test_t4_domain_service_calculates_due_dates_by_borrower_type() -> None:
    # T4 - BR4: STUDENT loans last 14 days and STAFF loans last 28 days.
    # Arrange
    service = LoanDueDateService()
    borrowed_on = date(2026, 10, 1)

    # Act
    student_due_date = service.calculate_due_date(borrowed_on, BorrowerType.STUDENT)
    staff_due_date = service.calculate_due_date(borrowed_on, BorrowerType.STAFF)

    # Assert
    assert student_due_date == date(2026, 10, 15)
    assert staff_due_date == date(2026, 10, 29)
