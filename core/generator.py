import pandas as pd
from core.categorizer import extract_entities, categorize, base_priority, guess_area

def to_gherkin(title: str, steps: list, expected: str) -> str:
    lines = [f"Scenario: {title}", f"  Given {steps[0]}"]
    for s in steps[1:-1]:
        lines.append(f"  When {s}")
    lines.append(f"  Then {expected}")
    return "\n".join(lines)

def make_test_variants(req: str, ents: dict) -> list:
    cases = []
    area = guess_area(req, ents)

    happy = {
        "title": f"Happy Path — {req[:40]}",
        "steps": ["system ready", "valid input provided", "action performed"],
        "expected": "success message shown",
        "priority": base_priority(req, ents),
        "area": area
    }
    cases.append(happy)

    if ents["has_validation"]:
        cases.append({
            "title": f"Validation — {req[:40]}",
            "steps": ["system ready", "invalid input provided", "action attempted"],
            "expected": "error message shown",
            "priority": "Medium",
            "area": area
        })
    return cases

def materialize_cases(requirements: list, style: str) -> pd.DataFrame:
    rows = []
    for i, req in enumerate(requirements, 1):
        ents = extract_entities(req)
        variants = make_test_variants(req, ents)
        for v in variants:
            cats = categorize(v["steps"], req, ents)
            if style == "Gherkin":
                steps_fmt = to_gherkin(v["title"], v["steps"], v["expected"])
                expected_fmt = ""
            else:
                steps_fmt = "\n".join([f"{idx+1}. {s}" for idx, s in enumerate(v["steps"])])
                expected_fmt = v["expected"]

            rows.append({
                "Req #": i,
                "Requirement": req,
                "Title": v["title"],
                "Steps" if style=="Manual" else "Gherkin": steps_fmt,
                "Expected Result" if style=="Manual" else "": expected_fmt,
                "Category": ", ".join(cats),
                "Priority": v["priority"],
                "Area": v["area"]
            })
    df = pd.DataFrame(rows)
    if "" in df.columns:  # cleanup empty column
        df = df.drop(columns=[""])
    return df
