# Library-Book-Borrowing-System
A Python project organized using Domain-Driven Design, TDD and Clean Architecture. It has two connected use cases: Borrow Book and Return Book. Storage is in memory.

# Layers
domain: aggregates, entities, value objects, the domain service, the domain event, and repository contracts
application: use cases, DTOs, and the event handler
infrastructure: in-memory repository implementations
presentation: the console interface
Dependencies point inward: presentation and infrastructure depend on application/domain, while domain depends on no framework.

Each class has its own file named after the class. A child entity lives in its own folder inside its aggregate, with its own value_objects/ when it needs them.
