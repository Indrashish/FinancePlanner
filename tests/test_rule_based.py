from categorizer.rule_based import RuleBasedCategorizer


def test_categorizes_sample_merchants():
    categorizer = RuleBasedCategorizer()

    assert categorizer.categorize("SPROUTS FARMERS MAR") == "Groceries"
    assert categorizer.categorize("COSTCO GAS #1662") == "Transportation"
    assert categorizer.categorize("SUPERCUTS") == "Personal Care"
    assert categorizer.categorize("TST*MARYS PIZZA SHACK") == "Restaurants"
