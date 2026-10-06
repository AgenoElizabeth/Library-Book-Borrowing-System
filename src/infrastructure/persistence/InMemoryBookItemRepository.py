"""An in-memory implementation of BookItemRepository."""

from copy import deepcopy

from src.domain.book_items.BookItem import BookItem
from src.domain.book_items.repositories.BookItemRepository import BookItemRepository

class InMemoryBookItemRepository(BookItemRepository):
    """Store BookItem aggregates in a dictionary.

    Copies are stored and returned, so unsaved changes never reach storage.
    """

    def __init__(self) -> None:
        self._book_items: dict[str, BookItem] = {}