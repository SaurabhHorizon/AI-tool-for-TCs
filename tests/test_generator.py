import pandas as pd
from core.generator import materialize_cases

REQS = [
    "User can login with email and password",
    "Invalid email format should show an error",
    "Admin can create a new product",
]

def test_materialize_cases_manual():
    df = materialize_cases(REQS, style="Manual")
    assert isinstance(df, pd.DataFrame)
    # Must contain core columns
    for col in ["Req #", "Requirement", "Title", "Category", "Priority", "Area", "Expected Result", "Steps"]:
        assert col in df.columns
    # Non-empty
    assert len(df) >= len(REQS)

def test_materialize_cases_gherkin():
    df = materialize_cases(REQS, style="Gherkin (Given-When-Then)")
    for col in ["Req #", "Requirement", "Title", "Category", "Priority", "Area", "Gherkin"]:
        assert col in df.columns
