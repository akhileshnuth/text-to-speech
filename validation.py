MAX_LENGTH = 20000 # Maximum allowed length for text inputs


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


def clean_and_validate_text(text: str) -> str:
    """
    - Strips spaces
    - Removes control characters
    - Checks emptiness and length
    """
    if text is None:
        raise ValidationError("Text cannot be empty.")

    # Remove control characters except common whitespace
    cleaned = "".join(
        ch for ch in text
        if (ord(ch) >= 32) or ch in ("\n", "\r", "\t")
    )

    cleaned = cleaned.strip()

    if not cleaned:
        raise ValidationError("Text cannot be empty after cleaning.")

    if len(cleaned) > MAX_LENGTH:
        raise ValidationError(f"Text is too long. Max {MAX_LENGTH} characters allowed.")

    return cleaned
