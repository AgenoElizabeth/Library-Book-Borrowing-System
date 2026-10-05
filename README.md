# Library Borrowing System

A Python project organized using Domain-Driven Design, TDD and Clean Architecture.
It has two connected use cases: **Borrow Book** and **Return Book**. Storage is in memory.

## Layers

- `domain`: aggregates, entities, value objects, the domain service, the domain event, and repository contracts
- `application`: use cases, DTOs, and the event handler
- `infrastructure`: in-memory repository implementations
- `presentation`: the console interface

Dependencies point inward: presentation and infrastructure depend on application/domain, while domain depends on no framework.

Each class has its own file named after the class. A child entity lives in its own
folder inside its aggregate, with its own `value_objects/` when it needs them.

```text
src/
├── domain/
│   ├── shared/
│   │   ├── AggregateRoot.py                 Layer Supertype
│   │   ├── DomainEvent.py                   Layer Supertype
│   │   └── Entity.py                        Layer Supertype
│   ├── book_items/
│   │   ├── BookItem.py                      Aggregate root A (BR2)
│   │   ├── value_objects/
│   │   │   ├── BookItemStatus.py
│   │   │   └── ISBN.py                      Value object (BR1)
│   │   ├── events/
│   │   │   └── BookBorrowed.py              Domain event (BR5)
│   │   └── repositories/
│   │       └── BookItemRepository.py        Repository contract (BR6)
│   └── borrower_accounts/
│       ├── BorrowerAccount.py               Aggregate root B (BR3)
│       ├── borrowings/
│       │   └── Borrowing.py                 Child entity
│       ├── value_objects/
│       │   └── BorrowerType.py
│       ├── services/
│       │   └── LoanDueDateService.py        Domain service (BR4)
│       └── repositories/
│           └── BorrowerAccountRepository.py Repository contract
├── application/
│   └── borrowing/
│       ├── BorrowBookApplicationService.py  Main use case
│       ├── ReturnBookApplicationService.py  Second use case
│       ├── BookBorrowedHandler.py           Event handler (BR5)
│       ├── DomainEventHandler.py            Handler contract
│       ├── BorrowBookInputDTO.py
│       ├── BorrowBookOutputDTO.py
│       ├── ReturnBookInputDTO.py
│       └── ReturnBookOutputDTO.py
├── infrastructure/
│   └── persistence/
│       ├── InMemoryBookItemRepository.py
│       └── InMemoryBorrowerAccountRepository.py
└── presentation/
    └── console.py                           Entry point and dependency wiring
```

## Run locally

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
```

Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Test

```bash
pytest
```

Saved test output: [evidence/test_output.txt](evidence/test_output.txt).

If ROS (or another tool) adds its own pytest plugins through `PYTHONPATH`, run
`env -u PYTHONPATH pytest` instead.

## Run the console application

```bash
python -m src.presentation.console
```
## Business rules and tests

| Rule | Type | Statement | Responsible | Tests |
|------|------|-----------|-------------|-------|
| BR1 | Value | ISBN must be a valid ISBN-13 | `ISBN` value object | T1, T2 |
| BR2 | Identity/State | A BookItem can be borrowed only when AVAILABLE | `BookItem` aggregate root | T3, T4 |
| BR3 | Invariant | Active borrowings must not exceed the borrowing limit | `BorrowerAccount` aggregate root | T5, T8 |
| BR4 | Cross-concept | Due date = borrowing date + loan days for the borrower type | `LoanDueDateService` | T6 |
| BR5 | Follow-up | After a successful borrow, the borrowing is recorded in BorrowerAccount | `BookBorrowed` + `BookBorrowedHandler` | T7, T8 |
| BR6 | Lookup | The BookItem must exist before borrowing continues | `BookItemRepository` + `BorrowBookApplicationService` | T7 |