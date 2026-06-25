from __future__ import annotations

from pathlib import Path

import pandas as pd

from categorizer.rule_based import RuleBasedCategorizer
from reader.statement_spreadsheet_reader import StatementSpreadsheetReader
from reporting.excel_report import ExcelReportWriter


class ExpenseAgent:
    """Agent that converts the user's bank-statement spreadsheet into a report.

    Current MVP behavior:
    - Read the provided workbook format.
    - Normalize transaction columns.
    - Use existing categories when present.
    - Categorize missing categories with simple rules.
    - Generate a transaction sheet and category summary sheet.
    """

    REQUIRED_COLUMNS = ["Merchant", "Amount"]

    def __init__(self):
        self.reader = StatementSpreadsheetReader()
        self.categorizer = RuleBasedCategorizer()
        self.report_writer = ExcelReportWriter()

    def process(
        self,
        input_path: str | Path,
        output_path: str | Path,
        *,
        recategorize_all: bool = False,
        prefer_raw_text: bool = False,
    ) -> pd.DataFrame:
        transactions = self.reader.read(input_path, prefer_raw_text=prefer_raw_text)
        transactions = self._validate(transactions)
        transactions = self._categorize(transactions, recategorize_all=recategorize_all)
        self.report_writer.write(transactions, output_path)
        return transactions

    def _validate(self, df: pd.DataFrame) -> pd.DataFrame:
        missing = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        df = df.copy()
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        df = df.dropna(subset=["Amount"])
        df = df[df["Amount"] != 0]
        return df.reset_index(drop=True)

    def _categorize(self, df: pd.DataFrame, *, recategorize_all: bool = False) -> pd.DataFrame:
        df = df.copy()

        if "Category" not in df.columns:
            df["Category"] = ""

        def choose_category(row: pd.Series) -> str:
            existing = str(row.get("Category", "")).strip()
            if not recategorize_all and existing and existing.lower() != "nan":
                return existing

            return self.categorizer.categorize(
                merchant=str(row.get("Merchant", "")),
                location=str(row.get("Location", "")),
                raw_description=str(row.get("Raw Description", "")),
            )

        df["Category"] = df.apply(choose_category, axis=1)
        return df
