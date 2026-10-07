"""A rich and fault-tolerant console interface for the Library Borrowing System.

Wires dependencies, seeds 100 Computer Science book items and sample borrower accounts,
and provides interactive options to borrow, return, search, list books, and view account statuses.
Handles input normalization, smart ID formatting, and clear error messaging.
"""

import re
from src.application.borrowing.BookBorrowedHandler import BookBorrowedHandler
from src.application.borrowing.BorrowBookApplicationService import BorrowBookApplicationService
from src.application.borrowing.BorrowBookInputDTO import BorrowBookInputDTO
from src.application.borrowing.ReturnBookApplicationService import ReturnBookApplicationService
from src.application.borrowing.ReturnBookInputDTO import ReturnBookInputDTO
from src.domain.book_items.BookItem import BookItem
from src.domain.book_items.value_objects.ISBN import ISBN
from src.domain.borrower_accounts.BorrowerAccount import BorrowerAccount
from src.domain.borrower_accounts.services.LoanDueDateService import LoanDueDateService
from src.domain.borrower_accounts.value_objects.BorrowerType import BorrowerType
from src.infrastructure.persistence.InMemoryBookItemRepository import InMemoryBookItemRepository
from src.infrastructure.persistence.InMemoryBorrowerAccountRepository import InMemoryBorrowerAccountRepository

CS_TITLES = [
    "Clean Code: A Handbook of Agile Software Craftsmanship",
    "Introduction to Algorithms (CLRS)",
    "Structure and Interpretation of Computer Programs (SICP)",
    "Design Patterns: Elements of Reusable Object-Oriented Software",
    "The Pragmatic Programmer: Your Journey to Mastery",
    "Artificial Intelligence: A Modern Approach",
    "Computer Systems: A Programmer's Perspective",
    "Operating System Concepts",
    "Computer Networking: A Top-Down Approach",
    "Compilers: Principles, Techniques, and Tools (Dragon Book)",
    "Database System Concepts",
    "Code Complete: A Practical Handbook of Software Construction",
    "The Art of Computer Programming: Fundamental Algorithms",
    "Head First Design Patterns",
    "Refactoring: Improving the Design of Existing Code",
    "Domain-Driven Design: Tackling Complexity in the Heart of Software",
    "Designing Data-Intensive Applications",
    "Computer Architecture: A Quantitative Approach",
    "Modern Operating Systems",
    "Algorithms (Sedgewick & Wayne)",
    "Python Crash Course",
    "Fluent Python: Clear, Concise, and Effective Programming",
    "Learning Python",
    "Programming Pearls",
    "The C Programming Language (K&R)",
    "Effective Java",
    "You Don't Know JS Yet: Scope & Closures",
    "Automate the Boring Stuff with Python",
    "Cracking the Coding Interview",
    "Grokking Algorithms: An Illustrated Guide",
    "Software Engineering at Google",
    "System Design Interview: An Insider's Guide",
    "Clean Architecture: A Craftsman's Guide to Software Structure",
    "Working Effectively with Legacy Code",
    "The Clean Coder: A Code of Conduct for Professional Programmers",
    "Distributed Systems: Principles and Paradigms",
    "Concepts, Techniques, and Models of Computer Programming",
    "Introduction to the Theory of Computation",
    "Pattern-Oriented Software Architecture",
    "Enterprise Integration Patterns",
]


def generate_isbn(index: int) -> ISBN:
    """Generate a valid ISBN-13 string for book seeding."""
    prefix = f"978013235{index:03d}"  # 12 digits
    total = sum(int(d) * (1 if pos % 2 == 0 else 3) for pos, d in enumerate(prefix))
    check_digit = (10 - (total % 10)) % 10
    return ISBN(f"{prefix}{check_digit}")

def seed_data(book_items: InMemoryBookItemRepository, borrower_accounts: InMemoryBorrowerAccountRepository) -> None:
    """Seed 100 Computer Science book items and diverse borrower accounts into memory."""
    for i in range(1, 101):
        book_id = f"BI{i:03d}"
        isbn = generate_isbn(i)
        title = CS_TITLES[(i - 1) % len(CS_TITLES)]
        book_items.save(BookItem(book_id, isbn, title=title))

    for i in range(1, 11):
        student_id = f"ST{i:03d}"
        borrower_accounts.save(BorrowerAccount(student_id, BorrowerType.STUDENT, borrowing_limit=3))
    borrower_accounts.save(BorrowerAccount("ST123", BorrowerType.STUDENT, borrowing_limit=3))

    for i in range(1, 6):
        staff_id = f"SF{i:03d}"
        borrower_accounts.save(BorrowerAccount(staff_id, BorrowerType.STAFF, borrowing_limit=5))


def normalize_book_id(raw_input: str) -> str:
    """Convert flexible input like '1', 'bi1', 'BI5' into standard 'BI001' format."""
    val = raw_input.strip().upper()
    if val.isdigit():
        return f"BI{int(val):03d}"
    match = re.match(r"^BI(\d+)$", val)
    if match:
        return f"BI{int(match.group(1)):03d}"
    return val    

def normalize_borrower_id(raw_input: str) -> str:
    """Convert flexible input like '1', 'st1', 'sf2' into standard 'ST001' or 'SF002' format."""
    val = raw_input.strip().upper()
    if val.isdigit():
        return f"ST{int(val):03d}"
    match_st = re.match(r"^ST(\d+)$", val)
    if match_st:
        return f"ST{int(match_st.group(1)):03d}"
    match_sf = re.match(r"^SF(\d+)$", val)
    if match_sf:
        return f"SF{int(match_sf.group(1)):03d}"
    return val


def parse_borrower_type(type_input: str, student_id: str) -> tuple[BorrowerType, int]:
    """Parse borrower category choice with smart fallback based on ID prefix."""
    val = type_input.strip().lower()
    if val in ("2", "staff", "stf", "f", "sf"):
        return BorrowerType.STAFF, 5
    if val in ("1", "student", "st", "s"):
        return BorrowerType.STUDENT, 3

    # Smart fallback based on Borrower ID prefix (SF -> STAFF, ST -> STUDENT)
    if student_id.upper().startswith("SF"):
        return BorrowerType.STAFF, 5
    return BorrowerType.STUDENT, 3