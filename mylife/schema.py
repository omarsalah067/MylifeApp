schema = {
    "$schema": "https://json-schema.org/draft/2019-09/schema",
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "pattern": "^[a-zA-Z ]+$",  # Only allows letters and spaces
            "minLength": 1,
            "maxLength": 25
        },
        "desc": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50  # Restrict to max 50 characters
        },
        "frequency": {
            "type": "string",
            "enum": ["daily", "weekly"]  # Only allows these two values
        },
        "completion dates": {
            "type": "array",
            "items": {"type": "string"},  # Ensures all items are strings (dates)
            "minItems": 0,
            "additionalItems": True
        }
    },
    "required": ["name", "desc", "frequency"]  # These fields must always be present
}
