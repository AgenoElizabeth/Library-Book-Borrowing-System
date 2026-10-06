"""The Borrow Book use case (main use case)."""

from collections.abc import Callable
from datetime import date

from src.application.borrowing.DomainEventHandler import DomainEventHandler
from src.application.borrowing.BorrowBookInputDTO import BorrowBookInputDTO
from src.application.borrowing.BorrowBookOutputDTO import BorrowBookOutputDTO
from src.domain.book_items.repositories.BookItemRepository import BookItemRepository
from src.domain.borrower_accounts.repositories.BorrowerAccountRepository import BorrowerAccountRepository
from src.domain.borrower_accounts.services.LoanDueDateService import LoanDueDateService

class BorrowBookApplicationService:
    """Coordinate the Borrow Book use case.

    The service holds no business rules. It loads aggregates, calls the domain,
    dispatches the Domain Event and saves the result. Every dependency is
    passed in from outside (Dependency Injection).
    """
    
    def __init__(
        self,
        book_items: BookItemRepository,
        borrower_accounts: BorrowerAccountRepository,
        due_date_service: LoanDueDateService,
        event_handler: DomainEventHandler,
        today: Callable[[], date] = date.today,
    ) -> None:
        self._book_items = book_items
        self._borrower_accounts = borrower_accounts
        self._due_date_service = due_date_service
        self._event_handler = event_handler
        self._today = today