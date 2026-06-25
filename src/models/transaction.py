from dataclasses import dataclass


@dataclass
class Transaction:
    transaction_date: str
    post_date: str
    merchant: str
    location: str
    amount: float
    category: str
    raw_description: str
