from pathlib import Path

from reader.statement_spreadsheet_reader import StatementSpreadsheetReader


def test_reads_sample_transactions_sheet():
    sample = Path("data/input/bank_statement_transactions.xlsx")
    reader = StatementSpreadsheetReader()

    df = reader.read(sample)

    assert len(df) == 50
    assert "Merchant" in df.columns
    assert "Amount" in df.columns
    assert df["Amount"].sum() > 3000
