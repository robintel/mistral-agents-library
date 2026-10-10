# Banking and Financial Services domain contract

Attaches to modernization, migration, and development tasks for financial
systems. Encodes the **rules, invariants, and pitfalls** that are specific to
banking and financial services, regardless of the technology stack. This
contract is **data, not agents** — it attaches alongside language and platform
contracts when the brief names a banking/finance context.

## The discipline

Banking systems are **not just software** — they are **financial instruments**
with legal, regulatory, and mathematical constraints that must be preserved
through any migration or modernization. A banking system that passes all
unit tests but breaks accounting rules is **not a banking system**.

- **Money is data with special properties**: it cannot be created or
  destroyed, only transferred; every transfer must balance; every
  transaction must be auditable.
- **Time is a first-class citizen**: transactions have timestamps,
  effective dates, value dates, and settlement dates; interest accrues
  continuously; end-of-day, end-of-month, and end-of-year are critical
  boundaries.
- **Auditability is mandatory**: every change to financial data must be
  traceable to a source (user, system, event) and a time; there must be
  no silent changes.
- **Reconciliation is the invariant**: at any point in time, the system
  must be able to reconcile its state against external systems (general
  ledger, central bank, payment networks) and internal records.
- **Compliance is non-negotiable**: regulations (Basel III, PCI-DSS,
  SOX, GDPR, PSD2, AML, KYC) are **requirements**, not features.

## Domain model

### Core entities

These are the fundamental business entities in banking, with their
invariant properties:

#### Account
- **Invariant**: Balance = Sum of all posted transactions ± pending
  transactions that have cleared
- **Properties**:
  - Account number/IBAN (unique identifier)
  - Account type (savings, checking, loan, etc.)
  - Currency (ISO 4217 code)
  - Balance (available, ledger, collected)
  - Status (active, closed, frozen, dormant)
  - Ownership (customer, joint, corporate)
  - Interest rate, terms, limits
  - Open date, close date
- **Constraints**:
  - Balance cannot be negative below overdraft limit
  - Closed accounts cannot have new transactions (except reversals)
  - Currency must be consistent for all transactions on the account

#### Customer
- **Invariant**: A customer is a legal entity with identity verification
- **Properties**:
  - Customer ID (internal identifier)
  - Name, address, contact information
  - Identification (passport, ID card, tax ID)
  - KYC (Know Your Customer) status and documents
  - Risk profile
  - Relationship manager
  - Accounts owned
- **Constraints**:
  - KYC must be complete and current before account opening
  - Customer data must be protected (PII, GDPR, data retention rules)
  - Customer must be uniquely identifiable

#### Transaction
- **Invariant**: Every transaction must balance (debit = credit) across
  the system
- **Properties**:
  - Transaction ID/reference (unique identifier)
  - Debit account, Credit account
  - Amount, Currency
  - Transaction type (deposit, withdrawal, transfer, payment, fee, interest)
  - Value date, Posting date, Settlement date
  - Status (pending, posted, cleared, reversed, failed)
  - Narrative/description
  - Related transactions (for reversals, corrections)
  - Channel (branch, ATM, mobile, online, API)
  - User/initiator
- **Constraints**:
  - Debit amount must equal credit amount (for transfers)
  - Value date ≤ Settlement date
  - Posting date is when transaction is recorded in the system
  - Settlement date is when funds are actually moved
  - Status transitions must be valid (pending → posted → cleared, etc.)

#### Payment
- **Invariant**: Payments are transactions with external parties
- **Properties**:
  - Payment ID
  - Sender account, Receiver account (or external party)
  - Amount, Currency
  - Payment method (ACH, wire, card, SEPA, SWIFT, etc.)
  - Payment network (Fedwire, CHIPS, SWIFT, local ACH)
  - Payment status (initiated, processed, settled, failed, returned)
  - Payment reference/end-to-end reference
  - Fee structure
- **Constraints**:
  - External payments must be reconciled with network statements
  - Payment fees must be correctly calculated and applied
  - Cross-border payments must handle FX (foreign exchange) correctly

#### Loan
- **Invariant**: Loan balance = Principal - Repayments + Interest accrued - Fees
- **Properties**:
  - Loan ID
  - Customer, Account
  - Loan type (personal, mortgage, auto, commercial)
  - Principal amount, Currency
  - Interest rate, Interest calculation method (simple, compound)
  - Term (start date, end date, maturity date)
  - Repayment schedule (amortization)
  - Collateral
  - Status (active, delinquent, defaulted, closed)
  - Disbursement date, First payment date
- **Constraints**:
  - Interest calculation must match contractual terms
  - Repayment schedule must cover principal + interest
  - Delinquency must be detected and handled per policy
  - Collateral value must be tracked

#### Deposit
- **Invariant**: Deposit balance + accrued interest = Customer's claim on bank
- **Properties**:
  - Deposit ID
  - Customer, Account
  - Deposit type (savings, term, CD)
  - Amount, Currency
  - Interest rate, Interest calculation frequency
  - Term (for term deposits)
  - Maturity date, Maturity instructions
  - Status (active, matured, closed)
- **Constraints**:
  - Early withdrawal penalties must be applied correctly
  - Interest must be calculated per contractual terms
  - Maturity instructions must be executed on maturity date

### Reference data

Data that defines the rules and parameters of the banking system:

- **Currency**: ISO 4217 codes, exchange rates, FX rules
- **Holidays**: Business holidays, non-working days, settlement calendars
- **Interest rates**: Base rates, customer-specific rates, rate curves
- **Fees**: Fee types, fee structures, fee waivers
- **Limits**: Transaction limits, daily limits, velocity limits
- **Products**: Product catalog, pricing, terms and conditions
- **Charts of accounts**: General ledger account structure
- **Branches**: Branch information, routing codes
- **Instruments**: Financial instruments (securities, derivatives, etc.)
- **Counterparties**: Banks, payment networks, clearing houses

## Invariants (the law)

These are the **non-negotiable rules** of banking systems:

### 1. Double-entry accounting
- **Rule**: Every financial transaction must have at least one debit and
  one credit entry that balance
- **Formula**: Σ(debits) = Σ(credits) for every transaction
- **Implication**: The system's total assets must always equal total
  liabilities + equity
- **Verification**: Run trial balance at end of each business day
- **Pitfall**: Single-entry updates that break the balance

### 2. No money creation/destruction
- **Rule**: The system cannot create or destroy money, only transfer it
- **Formula**: Total money in system at time T = Total money in system
  at time T-1
- **Implication**: Every debit must have a corresponding credit
- **Verification**: Balance sheet must always balance
- **Pitfall**: Orphaned transactions, missing credits/debits

### 3. Audit trail completeness
- **Rule**: Every change to financial data must be traceable
- **Properties**:
  - Who: User/system that made the change
  - What: The change that was made
  - When: Timestamp of the change
  - Why: Reason/business justification
  - Before/After: Previous and new values
- **Implication**: No direct database updates; all changes must go
  through audited interfaces
- **Verification**: Audit logs must be complete, immutable, and searchable
- **Pitfall**: Direct SQL updates, unlogged changes

### 4. Reconciliation
- **Rule**: The system must be able to reconcile its state with external
  systems and internal records
- **Types**:
  - **Internal reconciliation**: Between subsystems (e.g., core banking
    ↔ general ledger)
  - **External reconciliation**: With external parties (payment networks,
    correspondent banks)
  - **GL reconciliation**: General ledger must match all sub-ledgers
- **Frequency**: Daily for most reconciliations, intraday for critical
  systems
- **Verification**: Reconciliation reports must be generated and reviewed
- **Pitfall**: Unreconciled items, manual adjustments without documentation

### 5. Balance integrity
- **Rule**: Account balances must always reflect the true state
- **Formula**: Balance = Previous balance + Σ(credits) - Σ(debits) + interest
  - fees
- **Implication**: Balances must be calculated, not stored (or stored with
  calculation audit)
- **Verification**: Balance verification jobs must run regularly
- **Pitfall**: Storing balances without transaction history

### 6. Transaction finality
- **Rule**: Posted and settled transactions cannot be changed; they can
  only be reversed with a new transaction
- **Implication**: No updates to settled transactions; reversals must be
  new transactions with clear linkage
- **Verification**: Transaction status transitions must be irreversible
  (except for specific correction workflows)
- **Pitfall**: Modifying settled transactions, deleting transaction history

### 7. Interest calculation accuracy
- **Rule**: Interest must be calculated according to contractual terms and
  applicable regulations
- **Methods**:
  - Simple interest: I = P × r × t
  - Compound interest: A = P × (1 + r/n)^(nt)
  - Daily balance method
  - Average balance method
- **Implication**: Interest calculation must be auditable and verifiable
- **Verification**: Interest calculation must be tested with known cases
- **Pitfall**: Incorrect day count conventions, rounding errors

## Business processes

### Core banking processes

#### 1. Account Opening
**Purpose**: Create a new customer account
**Steps**:
1. KYC verification
2. Customer information collection
3. Account configuration (type, currency, limits)
4. Initial deposit (if applicable)
5. Account activation
**Invariants**:
- KYC must be complete before account creation
- Account number must be unique
- Initial deposit must be verified
**Reconciliation**: Account opening log vs. customer master

#### 2. Deposit
**Purpose**: Add funds to an account
**Steps**:
1. Validate customer and account
2. Validate deposit amount and currency
3. Create deposit transaction
4. Update account balance
5. Generate receipt
**Invariants**:
- Deposit amount must be positive
- Currency must match account currency
- Account must be active
**Reconciliation**: Deposit transactions vs. teller cash reports

#### 3. Withdrawal
**Purpose**: Remove funds from an account
**Steps**:
1. Validate customer and account
2. Check available balance
3. Check withdrawal limits
4. Create withdrawal transaction
5. Update account balance
6. Dispense cash/instruments
**Invariants**:
- Withdrawal amount cannot exceed available balance + overdraft
- Account must be active and not frozen
- Withdrawal must be authorized
**Reconciliation**: Withdrawal transactions vs. ATM/cash reports

#### 4. Transfer
**Purpose**: Move funds between accounts
**Steps**:
1. Validate source and destination accounts
2. Check available balance in source
3. Check limits (amount, frequency)
4. Create debit transaction for source
5. Create credit transaction for destination
6. Update both account balances atomically
**Invariants**:
- Debit = Credit (same amount)
- Both accounts must exist and be active
- Transaction must be atomic (both succeed or both fail)
**Reconciliation**: Transfers vs. account balances

#### 5. Payment Processing
**Purpose**: Send funds to external parties
**Steps**:
1. Validate payment request
2. Check account balance and limits
3. Check sanctions/aml screening
4. Create payment transaction
5. Send to payment network
6. Update account balance when settled
**Invariants**:
- Payment must be authorized
- Funds must be available
- Payment must comply with regulations
**Reconciliation**: Payments vs. payment network statements

#### 6. End of Day (EOD)
**Purpose**: Close business day and update ledgers
**Steps**:
1. Stop new transactions
2. Run batch processes (interest calculation, fee application, etc.)
3. Post GL entries
4. Generate reports (trial balance, position reports, etc.)
5. Reconcile all subsystems
6. Archive data
7. Start new business day
**Invariants**:
- EOD must be atomic and idempotent (can be rerun)
- All transactions for the day must be processed
- GL must balance
**Reconciliation**: All subsystems vs. GL

#### 7. End of Month (EOM)
**Purpose**: Close accounting month
**Steps**:
1. Run EOD for last day of month
2. Calculate monthly interest
3. Apply month-end accruals
4. Generate financial statements
5. Reconcile with external systems
6. Close month in GL
**Invariants**:
- Financial statements must be accurate
- All month-end adjustments must be documented
- Month must be closed before next month begins
**Reconciliation**: Financial statements vs. GL vs. external reports

#### 8. End of Year (EOY)
**Purpose**: Close accounting year
**Steps**:
1. Run EOM for December
2. Calculate annual interest
3. Apply year-end accruals and adjustments
4. Generate annual financial statements
5. Prepare for audit
6. Archive year data
**Invariants**:
- Annual financial statements must be auditable
- All year-end processes must be complete before year close
- Data must be archived according to retention policies
**Reconciliation**: Annual statements vs. monthly statements vs. GL

### Lending processes

#### 1. Loan Origination
**Purpose**: Create a new loan
**Steps**:
1. Customer application
2. Credit scoring and underwriting
3. Approval/rejection
4. Loan documentation
5. Disbursement
**Invariants**:
- Credit scoring must be documented
- Loan terms must be approved
- Disbursement must be authorized
**Reconciliation**: Loan disbursements vs. loan accounts

#### 2. Loan Servicing
**Purpose**: Manage existing loans
**Steps**:
1. Payment processing
2. Interest calculation
3. Late fee assessment
4. Delinquency management
5. Collection activities
**Invariants**:
- Payments must be applied correctly (principal vs. interest)
- Interest must be calculated per loan terms
- Delinquency must be detected and escalated
**Reconciliation**: Loan payments vs. loan balances

#### 3. Loan Closure
**Purpose**: Close a loan (full repayment or write-off)
**Steps**:
1. Final payment or write-off decision
2. Calculate final balance
3. Close loan account
4. Generate closure documents
**Invariants**:
- Final balance must be zero (or written off)
- Closure must be documented
- All fees and interest must be collected
**Reconciliation**: Closed loans vs. loan master

### Payment network processes

#### 1. ACH Processing
**Purpose**: Process Automated Clearing House transactions
**Steps**:
1. Receive ACH file
2. Validate file format and contents
3. Process individual transactions
4. Post to customer accounts
5. Generate return file for rejected transactions
6. Reconcile with ACH network
**Invariants**:
- File format must comply with ACH standards
- Each transaction must be validated
- Returns must be generated within time limits
**Reconciliation**: ACH transactions vs. ACH network statements

#### 2. Wire Transfer Processing
**Purpose**: Process high-value, real-time payments
**Steps**:
1. Receive wire transfer request
2. Validate customer and funds availability
3. Screen for sanctions/aml
4. Send to wire network (Fedwire, CHIPS, SWIFT)
5. Post to accounts when settled
6. Generate confirmation
**Invariants**:
- Wire must be processed in real-time
- Funds must be available before sending
- Screening must be complete
**Reconciliation**: Wire transfers vs. wire network statements

#### 3. Card Processing
**Purpose**: Process debit/credit card transactions
**Steps**:
1. Receive authorization request
2. Validate card and customer
3. Check available balance/credit limit
4. Send to card network (Visa, Mastercard, etc.)
5. Receive authorization response
6. Post transaction if authorized
7. Settle with card network
**Invariants**:
- Authorization must be obtained before posting
- Settlement must match authorizations
- Card network fees must be applied
**Reconciliation**: Card transactions vs. card network statements

## Data patterns

### Transaction data

#### Immutable transaction log
- **Pattern**: All transactions are immutable once posted
- **Implementation**: Append-only transaction table
- **Benefits**: Audit trail, historical analysis, replay capability
- **Pitfalls**: Storage growth, query performance
- **Mitigations**: Archive old transactions, use partitioning

#### Transaction journal
- **Pattern**: Separate journal table for transaction changes
- **Implementation**: Before/after images for each transaction update
- **Benefits**: Complete audit trail, ability to reconstruct state
- **Pitfalls**: Performance overhead
- **Mitigations**: Batch journal updates, optimize for common cases

### Balance calculation

#### Stored balances with calculation audit
- **Pattern**: Store current balance, but also store calculation method
  and parameters
- **Implementation**: Balance = f(transactions, interest rules, fees)
- **Benefits**: Performance (no recalculation), auditability
- **Pitfalls**: Calculation errors, balance drift
- **Mitigations**: Regular balance verification, reconciliation

#### On-demand balance calculation
- **Pattern**: Calculate balance from transactions when needed
- **Implementation**: SELECT SUM(amount) FROM transactions WHERE account_id = ?
- **Benefits**: Always accurate, no storage of derived data
- **Pitfalls**: Performance (slow for high-volume accounts)
- **Mitigations**: Cache calculated balances, use materialized views

### Reconciliation data

#### Reconciliation items table
- **Pattern**: Track all items that need reconciliation
- **Implementation**: Table with source, target, amount, date, status
- **Benefits**: Centralized reconciliation tracking
- **Pitfalls**: Complexity of matching logic
- **Mitigations**: Automated matching, exception-based review

#### Reconciliation history
- **Pattern**: Track reconciliation results over time
- **Implementation**: Reconciliation run log with statistics
- **Benefits**: Trend analysis, audit trail
- **Pitfalls**: Storage growth
- **Mitigations**: Archive old reconciliation data

## Common pitfalls

### Accounting pitfalls
- **Broken double-entry**: Transactions that don't balance
  - *Detection*: Trial balance doesn't balance
  - *Prevention*: Enforce debit = credit in transaction creation
- **Orphaned transactions**: Transactions without corresponding debit/credit
  - *Detection*: Reconciliation finds unmatched items
  - *Prevention*: Atomic transaction creation, validation
- **Incorrect posting dates**: Transactions posted to wrong accounting period
  - *Detection*: Period-end reconciliation fails
  - *Prevention*: Date validation, period locks
- **Balance drift**: Stored balance doesn't match calculated balance
  - *Detection*: Balance verification job finds discrepancies
  - *Prevention*: Regular balance recalculation, reconciliation
- **Missing GL entries**: Transactions not posted to general ledger
  - *Detection*: GL reconciliation finds missing entries
  - *Prevention*: Automatic GL posting, validation

### Interest calculation pitfalls
- **Incorrect day count**: Using wrong day count convention (30/360 vs. actual/365)
  - *Detection*: Interest test cases fail
  - *Prevention*: Use standard day count conventions, test with known cases
- **Rounding errors**: Different rounding methods cause discrepancies
  - *Detection*: Balance verification finds small differences
  - *Prevention*: Consistent rounding, use decimal arithmetic
- **Compounding errors**: Incorrect compounding frequency or method
  - *Detection*: Interest calculation test cases fail
  - *Prevention*: Clear documentation of compounding rules, testing
- **Rate errors**: Using wrong interest rate for customer/product
  - *Detection*: Customer complaints, audit findings
  - *Prevention*: Rate validation, effective date tracking

### Payment processing pitfalls
- **Duplicate payments**: Same payment processed multiple times
  - *Detection*: Reconciliation finds duplicate entries
  - *Prevention*: Idempotent payment processing, duplicate detection
- **Missing payments**: Payments not processed or posted
  - *Detection*: Reconciliation finds missing items
  - *Prevention*: Payment tracking, end-to-end monitoring
- **Incorrect FX rates**: Using wrong exchange rate for cross-border payments
  - *Detection*: FX gain/loss analysis finds discrepancies
  - *Prevention*: FX rate validation, timestamped rates
- **Settlement failures**: Payments sent but not settled
  - *Detection*: Settlement reconciliation finds unmatched items
  - *Prevention*: Settlement monitoring, retry logic

### Data migration pitfalls
- **Data loss**: Data not migrated from old to new system
  - *Detection*: Reconciliation finds missing data
  - *Prevention*: Comprehensive data mapping, validation
- **Data corruption**: Data migrated with incorrect values
  - *Detection*: Data quality checks fail
  - *Prevention*: Data validation, checksums, sampling
- **Incorrect mapping**: Data mapped to wrong fields/accounts
  - *Detection*: Business validation fails
  - *Prevention*: Clear mapping documentation, business rule testing
- **Timing issues**: Transactions posted with wrong timestamps
  - *Detection*: Transaction date validation fails
  - *Prevention*: Timestamp preservation, time zone handling

### Reconciliation pitfalls
- **False matches**: Items incorrectly matched in reconciliation
  - *Detection*: Manual review finds errors
  - *Prevention*: Multi-criteria matching, fuzzy matching with thresholds
- **Unmatched items**: Items that should match but don't
  - *Detection*: Reconciliation reports show unmatched items
  - *Prevention*: Data standardization, clear matching rules
- **Timing mismatches**: Items reconcile to different dates
  - *Detection*: Date-based reconciliation fails
  - *Prevention*: Consistent date handling, value date vs. posting date

## Compliance requirements

### Basel III
- **Purpose**: International regulatory framework for banks
- **Key requirements**:
  - Capital adequacy (CET1, Tier 1, Total capital ratios)
  - Liquidity coverage ratio (LCR)
  - Net stable funding ratio (NSFR)
  - Leverage ratio
  - Risk-weighted assets calculation
- **Implementation**:
  - Capital calculation engine
  - Risk-weighted asset calculation
  - Regulatory reporting
  - Stress testing

### PCI-DSS
- **Purpose**: Payment Card Industry Data Security Standard
- **Key requirements**:
  - Secure cardholder data storage
  - Encryption of cardholder data in transit
  - Access control to cardholder data
  - Regular monitoring and testing
  - Information security policy
- **Implementation**:
  - Tokenization of card data
  - Encryption at rest and in transit
  - Access controls and audit logging
  - Regular vulnerability scanning
  - Incident response plan

### SOX (Sarbanes-Oxley)
- **Purpose**: Corporate governance and financial reporting
- **Key requirements**:
  - Accurate financial reporting
  - Internal controls over financial reporting
  - Management certification of controls
  - Independent audit
- **Implementation**:
  - Financial controls framework
  - Segregation of duties
  - Change management for financial systems
  - Documentation of controls
  - Regular testing of controls

### GDPR
- **Purpose**: General Data Protection Regulation (EU)
- **Key requirements**:
  - Lawful basis for processing personal data
  - Data minimization
  - Data subject rights (access, rectification, erasure)
  - Data breach notification
  - Privacy by design and by default
- **Implementation**:
  - Personal data identification and classification
  - Consent management
  - Data subject request handling
  - Data retention and deletion policies
  - Privacy impact assessments

### PSD2 / Open Banking
- **Purpose**: Payment Services Directive 2 (EU) / Open Banking (UK)
- **Key requirements**:
  - Customer consent for data sharing
  - Secure APIs for third-party access
  - Strong customer authentication (SCA)
  - Account information services (AIS)
  - Payment initiation services (PIS)
- **Implementation**:
  - Open API platform
  - Consent management
  - SCA implementation
  - Developer portal
  - API monitoring and analytics

### AML (Anti-Money Laundering)
- **Purpose**: Prevent money laundering and terrorist financing
- **Key requirements**:
  - Customer due diligence (CDD)
  - Transaction monitoring
  - Suspicious activity reporting (SAR)
  - Sanctions screening
  - Record keeping
- **Implementation**:
  - KYC (Know Your Customer) processes
  - Transaction monitoring system
  - Sanctions screening against watchlists
  - SAR filing process
  - Audit trail for all AML activities

### KYC (Know Your Customer)
- **Purpose**: Verify customer identity and assess risk
- **Key requirements**:
  - Customer identification
  - Customer verification
  - Risk assessment
  - Ongoing monitoring
  - Record keeping
- **Implementation**:
  - Customer onboarding workflow
  - Document collection and verification
  - Risk scoring
  - Periodic review
  - Customer data management

## Testing patterns

### Transaction testing
- **Test double-entry**: Verify debit = credit for each transaction
- **Test balance integrity**: Verify account balance = Σ(transactions)
- **Test atomicity**: Verify transactions are atomic (all or nothing)
- **Test idempotency**: Verify same transaction can be retried safely
- **Test reversal**: Verify transaction reversal works correctly

### End-of-day testing
- **Test EOD completion**: Verify EOD completes successfully
- **Test EOD idempotency**: Verify EOD can be rerun without errors
- **Test GL balance**: Verify GL balances after EOD
- **Test report generation**: Verify all reports are generated
- **Test data archiving**: Verify data is archived correctly

### Reconciliation testing
- **Test reconciliation completion**: Verify reconciliation completes
- **Test reconciliation accuracy**: Verify all items are matched correctly
- **Test unmatched items**: Verify unmatched items are identified
- **Test reconciliation reporting**: Verify reports are accurate
- **Test data consistency**: Verify data is consistent across systems

### Interest calculation testing
- **Test simple interest**: Verify simple interest calculation
- **Test compound interest**: Verify compound interest calculation
- **Test day count**: Verify day count convention is correct
- **Test rounding**: Verify rounding is consistent
- **Test accrual**: Verify interest accrues correctly over time

### Performance testing
- **Test transaction throughput**: Verify system can handle required TPS
- **Test batch processing**: Verify batch jobs complete within time windows
- **Test end-of-day processing**: Verify EOD completes within time limits
- **Test concurrent users**: Verify system handles required concurrent users
- **Test data volume**: Verify system handles required data volumes

### Security testing
- **Test authentication**: Verify authentication mechanisms
- **Test authorization**: Verify authorization and access controls
- **Test encryption**: Verify data is encrypted at rest and in transit
- **Test audit logging**: Verify all changes are audited
- **Test vulnerability scanning**: Verify system passes vulnerability scans

## Best practices

### Development
- **Use domain-specific types**: Money, Currency, Amount, Balance (not
  primitive types)
- **Use decimal arithmetic**: Never use floating point for financial
  calculations (use BigDecimal, fixed-point, or decimal libraries)
- **Implement validation**: Validate all inputs, outputs, and state changes
- **Implement audit logging**: Log all changes to financial data
- **Implement reconciliation**: Regular reconciliation between systems
- **Use immutable data**: Transactions and other financial data should be
  immutable
- **Implement idempotency**: Operations should be idempotent (can be
  retried safely)
- **Implement atomicity**: Financial operations should be atomic

### Architecture
- **Separate domains**: Keep banking domain separate from other domains
- **Use domain-driven design (DDD)**: Model the banking domain accurately
- **Use event sourcing**: Store all changes as a sequence of events
- **Use CQRS**: Separate read and write models for performance and
  scalability
- **Implement saga pattern**: For distributed transactions that span
  multiple services
- **Use anti-corruption layer**: When integrating with external systems
  or legacy systems
- **Implement circuit breakers**: For external service calls to prevent
  cascading failures

### Data
- **Normalize carefully**: Balance normalization (reduce redundancy) with
  performance (joins can be expensive)
- **Use appropriate data types**: Money as decimal, dates with time zones,
  amounts with currency
- **Implement data retention**: Different retention periods for different
  data types (transaction data, customer data, etc.)
- **Implement data archiving**: Archive old data to maintain performance
- **Use appropriate indexing**: For fast query performance on common access
  patterns

### Operations
- **Implement batch processing**: For end-of-day, end-of-month, etc.
- **Use scheduling**: For regular batch jobs
- **Implement monitoring**: For system health, performance, errors
- **Implement alerting**: For critical issues (failed transactions, balance
  discrepancies, etc.)
- **Use appropriate SLAs**: For different types of operations (real-time
  vs. batch)

### Security
- **Implement defense in depth**: Multiple layers of security
- **Use principle of least privilege**: Minimal access for each user/system
- **Implement segregation of duties**: Separate duties to prevent fraud
- **Use encryption**: For data at rest and in transit
- **Implement key management**: Secure key storage and rotation
- **Use secure protocols**: TLS for communication, encrypted databases
- **Implement audit logging**: For all security-relevant events

## Domain-specific dialects

This contract attaches alongside other contracts when relevant:

- **Languages**: COBOL, Java, C#, Python, etc.
- **Platforms**: Mainframe (z/OS), Unix, Windows, cloud platforms
- **Stores**: IMS, VSAM, DB2, SQL databases, NoSQL databases
- **Brokers**: MQ Series, Kafka, RabbitMQ, etc.
- **Patterns**: ETL (for data migration), embedded (for ATM devices)

## Resources

- **Standards**: ISO 20022 (financial messaging), IFRS (accounting),
  GAAP (accounting)
- **Regulations**: Basel III, PCI-DSS, SOX, GDPR, PSD2, AML, KYC
- **Organizations**: SWIFT, Fedwire, CHIPS, local payment networks
- **Books**: "Banking Explained" by R. Barr, "The Principles of Banking"
  by Moorcroft
- **Certifications**: Certified Banking Professional, Chartered Financial
  Analyst (CFA)
- **Conferences**: Sibos, Money20/20, Finovate
