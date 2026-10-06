"""The Return Book use case."""

from src.application.borrowing.ReturnBookInputDTO import ReturnBookInputDTO
from src.application.borrowing.ReturnBookOutputDTO import ReturnBookOutputDTO
from src.domain.book_items.repositories.BookItemRepository import BookItemRepository
from src.domain.borrower_accounts.repositories.BorrowerAccountRepository import BorrowerAccountRepository


class ReturnBookApplicationService:
    """Coordinate the Return Book use case.

    Return Book completes the borrowing that BookBorrowed recorded. It raises no
    Domain Event because the system has exactly one.
    """
    
    def __init__(
        self,
        book_items: BookItemRepository,
        borrower_accounts: BorrowerAccountRepository,
    ) -> None:
        self._book_items = book_items
        self._borrower_accounts = borrower_accounts