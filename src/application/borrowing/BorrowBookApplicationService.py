"""The Borrow Book use case (main use case)."""

from collections.abc import Callable
from datetime import date

from src.application.borrowing.DomainEventHandler import DomainEventHandler
from src.application.borrowing.BorrowBookInputDTO import BorrowBookInputDTO
from src.application.borrowing.BorrowBookOutputDTO import BorrowBookOutputDTO
from src.domain.book_items.repositories.BookItemRepository import BookItemRepository
from src.domain.borrower_accounts.repositories.BorrowerAccountRepository import BorrowerAccountRepository
from src.domain.borrower_accounts.services.LoanDueDateService import LoanDueDateService

