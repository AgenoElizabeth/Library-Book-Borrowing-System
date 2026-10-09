# Test organization

Tests are grouped first by Clean Architecture layer and then by feature:

```text
tests/
├── domain/
│   ├── book_items/
│   │   ├── value_objects/test_isbn.py                T1
│   │   └── test_book_item.py                         T2
│   └── borrower_accounts/
│       ├── services/test_loan_due_date_service.py    T4
│       └── test_borrower_account.py                  T3
└── application/
    └── test_borrow_book.py                           T5-T8
```

Domain tests cover entities, value objects, and domain services without importing
application, infrastructure, or presentation code.

Application tests cover use cases through domain repository contracts. Test doubles
are defined in the test suite so application tests do not depend on concrete
infrastructure adapters.

The eight coursework tests are marked with `coursework`; run `pytest -m coursework`
to execute only T1-T8. Other tests remain in the suite as supplementary coverage.

These folders intentionally have no `__init__.py`: pytest discovers test modules by
filename and does not require the test directories to be importable packages.
