"""The BookBorrowedHandler (BR5 - Follow-up Rule)."""

from src.domain.book_items.events.BookBorrowed import BookBorrowed
from src.domain.borrower_accounts.repositories.BorrowerAccountRepository import BorrowerAccountRepository

class BookBorrowedHandler:
    """Ask Aggregate B (BorrowerAccount) to record the new active borrowing.

    BorrowerAccount checks BR3 before it accepts the borrowing. When the limit
    would be exceeded it raises ``ValueError`` and nothing is saved.
    """

    def __init__(self, borrower_accounts: BorrowerAccountRepository) -> None:
        self._borrower_accounts = borrower_accounts