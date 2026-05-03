# financeManager

A small ETL script that pulls bank transactions from the GoCardless (Nordigen) API and loads them into a MariaDB database. The focus is on reliability, simplicity, and safe re‑runs. The script handles token refresh, account discovery, transaction retrieval, and database insertion in one place.

The finance manager project is designed to autmatically pull transactional data from my bank account, and insert into a Database ready to be analysed
there are 3 compenants to the script, refreshing the access token, pulling the transactions, and inserting the transactions into the DB. This will be broken down
into 3 functions that will be called within the main function, it should avoid any hard coding for ease of use.

Python code: https://github.com/JBT41/financeManager/blob/main/blankfinanceManager.py

Goals

1.) Automatically refresh the access token (expires every 24hours)

2.) Automatically pull the previous days transactions from my bank account

3.) Automatically Insert the transactions into a Database

4.) Analyse the data using PowerBI or Grafana.

Technologies

1.) GoCardlessAPI

2.) Python

3.) Linux (ubuntu)

3.) MariaDB

## Overview

The script does the following:

- Refreshes the GoCardless access token using a stored refresh token
- Retrieves all accounts linked to a requisition
- Fetches transactions for each account
- Normalises the data into a consistent structure
- Inserts the results into MariaDB
- Avoids duplicates using a primary key on `internalTransactionId`
- Uses a single database transaction to prevent partial loads

The intention is to make the ETL safe to run on a schedule without worrying about half‑written data or duplicate rows.

## Project Structure

    financeManager/
    │
    ├── blankfinanceManager.py     # Main ETL script
    ├── requirements.txt           # Python dependencies
    └── README.md

A `.env` file is required for configuration but is not committed to the repository.

## Setup

### 1. Install dependencies

    pip install -r requirements.txt

### 2. Create a `.env` file

Example:

    HOST=localhost
    DATABASE=finance
    REQUISITION_ID=49093370-fb0a-4c36-bb98-20c486683583

### 3. Store secrets using keyring

Refresh token:

    keyring.set_password("refresh_token", "refresh_token", "<YOUR_REFRESH_TOKEN>")

Database credentials:

    keyring.set_password("MySQL", "username", "<DB_USER>")
    keyring.set_password("MySQL", "password", "<DB_PASS>")

This keeps sensitive values out of the code and out of the `.env` file.

## How the ETL Works

### Token refresh
The script retrieves the refresh token from keyring and exchanges it for a new access token before making any API calls.

### Account discovery
The requisition ID from `.env` is used to fetch all linked accounts. This avoids hard‑coding account numbers.

### Transaction retrieval
For each account, the script calls the GoCardless API and extracts the fields needed for the database.

### Database load
All inserts are wrapped in a single database transaction:

- If all rows succeed, the transaction is committed.
- If anything fails, the transaction is rolled back.

This prevents partial loads and keeps the table consistent.

### Duplicate protection
The table uses:

    PRIMARY KEY (internalTransactionId)

This ensures the ETL can be safely re‑run without inserting the same transaction twice.

## Database Schema

The script expects a table with fields similar to:

- transactionID  
- entryReference  
- bookingDate  
- valueDate  
- amount  
- currency  
- debtorName  
- creditorName  
- remittanceInformation  
- proprietaryBankTransactionCode  
- internalTransactionId (primary key)

The primary key is what guarantees idempotency.

## Running the Script

    python blankfinanceManager.py

If everything is configured correctly, the script will:

- refresh the token  
- fetch accounts  
- fetch transactions  
- load them into MariaDB  
- skip duplicates  
- avoid partial loads  

## Scheduling

### Windows Task Scheduler
Set up a daily trigger and point it at your Python executable and script path.

### Linux cron

    0 7 * * * /usr/bin/python3 /path/to/blankfinanceManager.py

## Future Improvements

- Logging to file
- Retry logic for API calls
- Email notifications on success/failure
- Docker support
- Unit tests
















