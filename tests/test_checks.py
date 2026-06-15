from src.checks import alcohol_content_check, net_contents_check, government_warning_check


def test_alcohol_content_check_passes_with_abv():
    text = "OLD TOM DISTILLERY 45% Alc./Vol. 750 mL"
    result = alcohol_content_check("45", text)
    assert result["status"] == "PASS"


def test_alcohol_content_check_passes_with_proof():
    text = "OLD TOM DISTILLERY 90 Proof 750 mL"
    result = alcohol_content_check("45", text)
    assert result["status"] == "PASS"


def test_net_contents_check_passes():
    text = "OLD TOM DISTILLERY Kentucky Straight Bourbon Whiskey 750 mL"
    result = net_contents_check("750 mL", text)
    assert result["status"] == "PASS"


def test_government_warning_fails_when_missing():
    text = "OLD TOM DISTILLERY Kentucky Straight Bourbon Whiskey"
    result = government_warning_check(text)
    assert result["status"] == "FAIL"
    