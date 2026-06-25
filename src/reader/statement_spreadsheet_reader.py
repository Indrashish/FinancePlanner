from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import pandas as pd


class StatementSpreadsheetReader:
    """Reads the user's bank statement spreadsheet format.

    Supported input formats:
    1. A structured `Transactions` sheet with columns like:
       Transaction Date, Post Date, Merchant, Location, Transaction ID,
       Card Last 4, Amount, Category.
    2. A `Raw Text` sheet containing original pasted statement lines.

    The structured sheet is preferred when available because it is cleaner.
    """

    TRANSACTIONS_SHEET = "Transactions"
    RAW_TEXT_SHEET = "Raw Text"

    STRUCTURED_COLUMNS = [
        "Transaction Date",
        "Post Date",
        "Merchant",
        "Location",
        "Transaction ID",
        "Card Last 4",
        "Amount",
        "Category",
    ]

    RAW_LINE_PATTERN = re.compile(
        r"^(?P<transaction_date>\d{2}/\d{2})\s+"
        r"(?P<post_date>\d{2}/\d{2})\s+"
        r"(?P<body>.+?)\s+"
        r"(?P<transaction_id>\d{4})\s+"
        r"(?P<card_last_4>\d{4})\s+"
        r"(?P<amount>-?\d+(?:\.\d{2})?)$"
    )

    def read(self, input_path: str | Path, prefer_raw_text: bool = False) -> pd.DataFrame:
        input_path = Path(input_path)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        excel = pd.ExcelFile(input_path)
        sheet_names = set(excel.sheet_names)

        if prefer_raw_text and self.RAW_TEXT_SHEET in sheet_names:
            return self._read_raw_text(excel)

        if self.TRANSACTIONS_SHEET in sheet_names:
            return self._read_transactions_sheet(excel)

        if self.RAW_TEXT_SHEET in sheet_names:
            return self._read_raw_text(excel)

        raise ValueError(
            f"Could not find '{self.TRANSACTIONS_SHEET}' or '{self.RAW_TEXT_SHEET}' sheet. "
            f"Available sheets: {excel.sheet_names}"
        )

    def _read_transactions_sheet(self, excel: pd.ExcelFile) -> pd.DataFrame:
        df = pd.read_excel(excel, sheet_name=self.TRANSACTIONS_SHEET)
        df = self._clean_column_names(df)

        rename_map = {
            "TransactionDate": "Transaction Date",
            "Transaction_Date": "Transaction Date",
            "PostDate": "Post Date",
            "Post_Date": "Post Date",
            "TransactionID": "Transaction ID",
            "Transaction_Id": "Transaction ID",
            "CardLast4": "Card Last 4",
            "Card_Last_4": "Card Last 4",
        }
        df = df.rename(columns=rename_map)

        for col in self.STRUCTURED_COLUMNS:
            if col not in df.columns:
                df[col] = "" if col != "Amount" else 0.0

        df = df[self.STRUCTURED_COLUMNS].copy()
        return self._finalize(df)

    def _read_raw_text(self, excel: pd.ExcelFile) -> pd.DataFrame:
        raw_df = pd.read_excel(excel, sheet_name=self.RAW_TEXT_SHEET, header=None)
        lines = [str(value).strip() for value in raw_df.iloc[:, 0].dropna().tolist()]
        rows = [self._parse_raw_line(line) for line in lines]
        rows = [row for row in rows if row is not None]

        if not rows:
            raise ValueError("No transaction rows could be parsed from the Raw Text sheet")

        df = pd.DataFrame(rows)
        return self._finalize(df)

    def _parse_raw_line(self, line: str) -> dict | None:
        match = self.RAW_LINE_PATTERN.match(line)
        if not match:
            return None

        data = match.groupdict()
        body = data["body"].strip()
        merchant, location = self._split_merchant_location(body)

        return {
            "Transaction Date": data["transaction_date"],
            "Post Date": data["post_date"],
            "Merchant": merchant,
            "Location": location,
            "Transaction ID": data["transaction_id"],
            "Card Last 4": data["card_last_4"],
            "Amount": data["amount"],
            "Category": "",
            "Raw Description": line,
        }

    def _split_merchant_location(self, body: str) -> tuple[str, str]:
        """Best-effort merchant/location split for raw statement lines.

        The sample format places merchant first and location near the end.
        This heuristic keeps it simple and can be tuned per bank later.
        """
        state_pattern = re.search(r"\b[A-Z]{2}\b", body)
        if state_pattern:
            before_state = body[: state_pattern.start()].strip()
            state_and_before = body[state_pattern.start() :].strip()
            parts = before_state.split()
            if len(parts) >= 2:
                # Put the last 1-3 location words with the state.
                location_words = parts[-3:]
                merchant_words = parts[:-3]
                if merchant_words:
                    return " ".join(merchant_words).strip(), f"{' '.join(location_words)} {state_and_before}".strip()
        return body, ""

    def _clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df.columns = [str(col).strip() for col in df.columns]
        return df

    def _finalize(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
        df = df.dropna(subset=["Amount"])

        for col in ["Transaction Date", "Post Date", "Merchant", "Location", "Transaction ID", "Card Last 4", "Category"]:
            if col in df.columns:
                df[col] = df[col].fillna("").astype(str).str.strip()

        if "Raw Description" not in df.columns:
            df["Raw Description"] = df.apply(
                lambda row: " ".join(
                    str(row.get(col, "")).strip()
                    for col in ["Transaction Date", "Post Date", "Merchant", "Location", "Transaction ID", "Card Last 4", "Amount"]
                ),
                axis=1,
            )

        return df.reset_index(drop=True)
