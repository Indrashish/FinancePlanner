# FinancePlanner
Creating a monthly financial tracker and planner

# Bank Expense Agent

## Overview

Bank Expense Agent is an AI-powered personal finance assistant that automatically extracts transactions from bank statement PDFs, categorizes expenses, and generates monthly spending reports in Excel format.

The goal of the project is to demonstrate an agentic workflow where an AI system can:

* Read bank statements
* Extract transaction information
* Categorize expenses
* Generate financial summaries
* Produce spreadsheet reports

---

## Features

### PDF Transaction Extraction

Extracts:

* Transaction Date
* Merchant Name
* Transaction Amount
* Debit/Credit Type

### Expense Categorization

Supported categories:

* Groceries
* Restaurants
* Utilities
* Transportation
* Shopping
* Healthcare
* Travel
* Entertainment
* Subscriptions
* Baby Expenses
* Other

Categorization can be performed using:

* Rule-based matching
* LLM-based classification

### Reporting

Generates:

* Transaction-level spreadsheet
* Monthly category summary
* Spending breakdown

---

## Architecture

PDF Statement
→ Statement Parser
→ Transaction Extractor
→ Expense Categorizer
→ Report Generator
→ Excel Summary

---

## Repository Structure

bank-expense-agent/

* src/

  * pdf_parser/
  * extractor/
  * categorizer/
  * spreadsheet/
  * agent/

* tests/

* docs/

* data/

---

## Installation

```bash
git clone <repository>
cd bank-expense-agent

pip install -r requirements.txt
```

---

## Run

```bash
python src/main.py
```

---

## Sample Workflow

Input:

Statement.pdf

Output:

monthly_expense_report.xlsx

Category Summary:

Groceries: $650

Restaurants: $420

Utilities: $180

Subscriptions: $75

---

## Future Enhancements

* Multi-bank support
* Automatic merchant normalization
* Budget tracking
* Spending trend analysis
* Email delivery of reports
* Conversational expense assistant
* Dashboard visualization

---

## Technologies

* Python
* pandas
* pdfplumber
* openpyxl
* OpenAI API (optional)
* pytest
