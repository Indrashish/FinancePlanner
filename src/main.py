from __future__ import annotations

import argparse
from pathlib import Path

from agent.expense_agent import ExpenseAgent


def main() -> None:
    parser = argparse.ArgumentParser(description="Bank Expense Agent")
    parser.add_argument(
        "--input",
        default="data/input/bank_statement_transactions.xlsx",
        help="Input spreadsheet path. Default: data/input/bank_statement_transactions.xlsx",
    )
    parser.add_argument(
        "--output",
        default="data/output/monthly_report.xlsx",
        help="Output Excel report path. Default: data/output/monthly_report.xlsx",
    )
    parser.add_argument(
        "--recategorize-all",
        action="store_true",
        help="Ignore existing Category values and categorize every transaction using rules.",
    )
    parser.add_argument(
        "--prefer-raw-text",
        action="store_true",
        help="Parse the Raw Text sheet instead of the structured Transactions sheet.",
    )
    args = parser.parse_args()

    agent = ExpenseAgent()
    transactions = agent.process(
        input_path=Path(args.input),
        output_path=Path(args.output),
        recategorize_all=args.recategorize_all,
        prefer_raw_text=args.prefer_raw_text,
    )

    print(f"Processed {len(transactions)} transactions")
    print(f"Report created: {args.output}")


if __name__ == "__main__":
    main()
