import os
import sys
import pytest

#  Add project root to sys.path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from validation import clean_and_validate_text, ValidationError


def test_valid_text():
    text = "Hello, this is a test."
    cleaned = clean_and_validate_text(text)
    assert cleaned == text


def test_empty_text_spaces():
    with pytest.raises(ValidationError):
        clean_and_validate_text("     ")


def test_none_text():
    with pytest.raises(ValidationError):
        clean_and_validate_text(None)


def test_too_long_text():
    long_text = "a" * 6000
    with pytest.raises(ValidationError):
        clean_and_validate_text(long_text)


def test_control_characters_removed():
    text = "Hello\x01World"
    cleaned = clean_and_validate_text(text)
    assert cleaned == "HelloWorld"
