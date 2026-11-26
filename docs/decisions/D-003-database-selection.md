# Decision 1: Database Selection for the Website

**Decision ID:** D-001  
**Date:** 25/11/2026  
**Status:** Accepted  
**Related:** Research Brief, Section 5.2

## 1. Context

The project requires a database management system for the e-commerce promotion personalization website.

The database should support the application's data structures, user management, and operational requirements while remaining feasible within the project's implementation timeline.

Two database management systems were considered: MongoDB and PostgreSQL.

## 2. Alternatives Considered

### Option 1: MongoDB

**Advantages:**
- Flexible document-based data model.
- Convenient integration with a JavaScript-based application stack.
- Suitable for storing application data with evolving document structures.

**Disadvantages:**
- Requires explicit schema validation to maintain data consistency.
- Relationships and complex queries may require additional design considerations.
- Transactional consistency must be configured carefully when multiple documents are involved.

### Option 2: PostgreSQL

**Advantages:**
- Relational data model with structured schemas.
- Strong support for constraints and transactions.
- Suitable for applications with complex relationships and relational queries.

**Disadvantages:**
- Requires careful relational schema design.
- May involve additional mapping between application objects and relational tables.

## 3. Decision

MongoDB is selected as the database management system for the website application.

The selection is subject to the following implementation conditions:

1. **Schema validation:** Define appropriate validation rules to maintain data consistency.
2. **Indexes:** Implement unique and compound indexes where required.
3. **Transactions:** Configure a replica set if multi-document transactions are needed.
4. **Auditability:** Maintain append-only records for important assignment, event, and consent activities where appropriate.

Research datasets and analytical data will be managed separately from the application database using appropriate research data formats and storage.

## 4. Rationale and Evidence

MongoDB is selected based on its flexible document model and compatibility with the planned JavaScript-based application stack.

The choice also considers the project's implementation scope, development timeline, and the need to keep application data separate from analytical datasets.

The selection does not imply that MongoDB is universally superior to PostgreSQL. It is a project-specific technical decision.

## 5. Consequences

**Benefits:**
- Provides flexibility for application data structures.
- Supports integration with the planned application architecture.
- Keeps operational application data separate from research datasets.

**Trade-offs and limitations:**
- Data validation and consistency require deliberate implementation.
- Index design and query performance must be considered.
- Transaction requirements may introduce additional configuration.

**Risks and mitigation:**
- Risk of inconsistent documents: implement schema validation.
- Risk of duplicate records: define appropriate unique indexes.
- Risk of inconsistent multi-document operations: use transactions where necessary.
- Risk of losing auditability: maintain appropriate append-only records.

## 6. Review

This decision may be revisited if application requirements change materially or implementation reveals limitations that cannot be addressed within the project's constraints.