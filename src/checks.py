import re
from rapidfuzz import fuzz


REQUIRED_WARNING = (
    "GOVERNMENT WARNING: "
    "(1) According to the Surgeon General, women should not drink alcoholic beverages "
    "during pregnancy because of the risk of birth defects. "
    "(2) Consumption of alcoholic beverages impairs your ability to drive a car or operate "
    "machinery, and may cause health problems."
)


def clean_text(text):
    if not text:
        return ""

    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fuzzy_field_check(expected, extracted_text, field_name, pass_threshold=85, review_threshold=70):
    expected_clean = clean_text(expected).lower()
    extracted_clean = clean_text(extracted_text).lower()

    if not expected_clean:
        return {
            "field": field_name,
            "status": "REVIEW",
            "expected": expected,
            "found": "",
            "score": 0,
            "notes": "No expected value was provided."
        }

    score = fuzz.partial_ratio(expected_clean, extracted_clean)

    if score >= pass_threshold:
        status = "PASS"
        notes = "Strong match found."
    elif score >= review_threshold:
        status = "REVIEW"
        notes = "Possible match found, but human review is recommended."
    else:
        status = "FAIL"
        notes = "Expected value was not clearly found on the label."

    return {
        "field": field_name,
        "status": status,
        "expected": expected,
        "found": "See OCR text",
        "score": round(score, 2),
        "notes": notes
    }


def extract_abv_values(text):
    text = clean_text(text)

    abv_patterns = [
        r"(\d{1,2}(?:\.\d+)?)\s*%\s*(?:alc\.?/vol\.?|abv|alcohol by volume)?",
        r"alc\.?/vol\.?\s*(\d{1,2}(?:\.\d+)?)\s*%",
        r"abv\s*(\d{1,2}(?:\.\d+)?)\s*%"
    ]

    found = []

    for pattern in abv_patterns:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        for match in matches:
            found.append(float(match))

    proof_matches = re.findall(r"(\d{2,3}(?:\.\d+)?)\s*proof", text, flags=re.IGNORECASE)
    for proof in proof_matches:
        proof_value = float(proof)
        found.append(proof_value / 2)

    return found


def alcohol_content_check(expected_abv, extracted_text):
    found_abvs = extract_abv_values(extracted_text)

    try:
        expected_number = float(re.findall(r"\d{1,2}(?:\.\d+)?", expected_abv)[0])
    except Exception:
        return {
            "field": "Alcohol Content",
            "status": "REVIEW",
            "expected": expected_abv,
            "found": str(found_abvs),
            "score": 0,
            "notes": "Could not parse expected alcohol content."
        }

    for value in found_abvs:
        if abs(value - expected_number) <= 0.5:
            return {
                "field": "Alcohol Content",
                "status": "PASS",
                "expected": expected_abv,
                "found": f"{value}% ABV",
                "score": 100,
                "notes": "Alcohol content matches expected value."
            }

    if found_abvs:
        return {
            "field": "Alcohol Content",
            "status": "FAIL",
            "expected": expected_abv,
            "found": ", ".join([f"{v}% ABV" for v in found_abvs]),
            "score": 0,
            "notes": "Alcohol content was found, but it does not match the expected value."
        }

    return {
        "field": "Alcohol Content",
        "status": "FAIL",
        "expected": expected_abv,
        "found": "",
        "score": 0,
        "notes": "No alcohol content was found on the label."
    }


def net_contents_check(expected_net_contents, extracted_text):
    text = clean_text(extracted_text)

    pattern = r"(\d+(?:\.\d+)?)\s*(ml|mL|ML|l|L|liter|liters)"
    matches = re.findall(pattern, text)

    found_values = [f"{amount} {unit}" for amount, unit in matches]

    expected_clean = clean_text(expected_net_contents).lower().replace(" ", "")
    found_clean = [value.lower().replace(" ", "") for value in found_values]

    if expected_clean in found_clean:
        status = "PASS"
        notes = "Net contents match expected value."
    elif found_values:
        status = "REVIEW"
        notes = "Net contents were found, but not an exact match."
    else:
        status = "FAIL"
        notes = "No net contents value was found."

    return {
        "field": "Net Contents",
        "status": status,
        "expected": expected_net_contents,
        "found": ", ".join(found_values),
        "score": 100 if status == "PASS" else 50 if status == "REVIEW" else 0,
        "notes": notes
    }


def government_warning_check(extracted_text):
    text = clean_text(extracted_text)

    warning_score = fuzz.partial_ratio(REQUIRED_WARNING.lower(), text.lower())
    has_caps_intro = "GOVERNMENT WARNING:" in text

    if warning_score >= 90 and has_caps_intro:
        status = "PASS"
        notes = "Government warning appears to match required wording and has all-caps introduction."
    elif warning_score >= 75:
        status = "REVIEW"
        notes = "Government warning appears partially present, but wording or capitalization should be reviewed."
    else:
        status = "FAIL"
        notes = "Required government warning was not clearly found."

    if not has_caps_intro:
        notes += " The required 'GOVERNMENT WARNING:' introduction was not found in all caps."

    return {
        "field": "Government Warning",
        "status": status,
        "expected": "Standard government warning statement",
        "found": "See OCR text",
        "score": round(warning_score, 2),
        "notes": notes
    }


def overall_status(results):
    statuses = [result["status"] for result in results]

    if "FAIL" in statuses:
        return "FAIL"
    if "REVIEW" in statuses:
        return "REVIEW"
    return "PASS"


def run_all_checks(expected_data, extracted_text):
    results = []

    results.append(
        fuzzy_field_check(
            expected_data.get("brand_name", ""),
            extracted_text,
            "Brand Name"
        )
    )

    results.append(
        fuzzy_field_check(
            expected_data.get("class_type", ""),
            extracted_text,
            "Class/Type"
        )
    )

    results.append(
        alcohol_content_check(
            expected_data.get("alcohol_content", ""),
            extracted_text
        )
    )

    results.append(
        net_contents_check(
            expected_data.get("net_contents", ""),
            extracted_text
        )
    )

    results.append(government_warning_check(extracted_text))

    return results
