import os
from core.parser import parse_input_text
from core.utils import clean_text

SAMPLE = """
- User can login with email and password.
- Password reset link shall be sent via email.
Invalid input should show proper error states.
"""

def test_parse_input_text_splits_lines():
    reqs = parse_input_text(SAMPLE)
    assert isinstance(reqs, list)
    assert any("login" in r.lower() for r in reqs)
    assert any("password reset" in r.lower() for r in reqs)
    assert any("invalid input" in r.lower() for r in reqs)

def test_clean_text_compacts_spaces():
    assert clean_text("  a   b \n c ") == "a b c"
