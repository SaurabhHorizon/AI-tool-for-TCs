CORE_KEYWORDS = {
    "auth": ["login", "logout", "signin"],
    "validation": ["invalid", "error", "empty", "required"],
    "crud": ["create", "update", "delete", "edit"],
}

def extract_entities(req: str) -> dict:
    return {
        "has_auth": any(k in req.lower() for k in CORE_KEYWORDS["auth"]),
        "has_validation": any(k in req.lower() for k in CORE_KEYWORDS["validation"]),
        "has_crud": any(k in req.lower() for k in CORE_KEYWORDS["crud"]),
    }

def base_priority(req: str, ents: dict) -> str:
    if ents["has_auth"]:
        return "High"
    if ents["has_validation"]:
        return "Medium"
    return "Low"

def guess_area(req: str, ents: dict) -> str:
    if ents["has_auth"]:
        return "Authentication"
    if ents["has_crud"]:
        return "CRUD"
    return "General"

def categorize(step_texts: list, req: str, ents: dict) -> list:
    cats = ["Functional"]
    if ents["has_auth"]:
        cats.append("Regression")
    if ents["has_validation"]:
        cats.append("Negative")
    return cats
