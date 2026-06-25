from __future__ import annotations


class RuleBasedCategorizer:
    """Simple merchant/category rules tuned for the provided sample file."""

    RULES: dict[str, list[str]] = {
        "Groceries": [
            "SPROUTS",
            "INDIA FRESH",
            "SAFEWAY",
            "TRADER JOE",
            "WHOLE FOODS",
            "GROCERY",
            "FARMERS MAR",
        ],
        "Restaurants": [
            "PIZZA",
            "STARBUCKS",
            "MCDONALD",
            "RESTAURANT",
            "CAFE",
            "SWEET SCOOPS",
            "TST*",
            "IKEA EAST PALO ALTO REST",
        ],
        "Transportation": [
            "GAS",
            "COSTCO GAS",
            "CHEVRON",
            "SHELL",
            "UBER",
            "LYFT",
            "PARKING",
        ],
        "Subscriptions": [
            "NETFLIX",
            "SPOTIFY",
            "APPLE.COM",
            "GOOGLE",
            "AMAZON PRIME",
            "MICROSOFT",
        ],
        "Healthcare": [
            "CVS",
            "WALGREENS",
            "KAISER",
            "PHARMACY",
            "MEDICAL",
            "DENTAL",
        ],
        "Utilities/Home": [
            "PG&E",
            "PGE",
            "UTILITY",
            "WATER",
            "INTERNET",
            "COMCAST",
            "AT&T",
            "HOME DEPOT",
        ],
        "Personal Care": [
            "SUPERCUTS",
            "SALON",
            "BARBER",
            "HAIRCUT",
        ],
        "Travel/Entertainment": [
            "HOTEL",
            "AIRBNB",
            "WINERY",
            "ROCHE WINERY",
            "MOVIE",
            "THEATRE",
            "AIRLINES",
        ],
        "Shopping": [
            "AMAZON",
            "TARGET",
            "WALMART",
            "BEST BUY",
            "COSTCO.COM",
            "IKEA EAST PALO ALTO",
            "IKEA",
        ],
    }

    def categorize(self, merchant: str, location: str = "", raw_description: str = "") -> str:
        text = f"{merchant} {location} {raw_description}".upper()

        for category, keywords in self.RULES.items():
            for keyword in keywords:
                if keyword.upper() in text:
                    return category

        return "Other"
