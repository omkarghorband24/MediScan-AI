import re


def extract_prescription_details(text):

    result = {
        "dose": [],
        "timing": [],
        "duration": []
    }

    # Dose Pattern (Example: 1-0-1)
    dose_pattern = r"\b\d-\d-\d\b"
    result["dose"] = re.findall(dose_pattern, text)

    # Timing Keywords
    timings = [
        "Before Food",
        "After Food",
        "Morning",
        "Afternoon",
        "Evening",
        "Night",
        "SOS"
    ]

    for timing in timings:
        if timing.lower() in text.lower():
            result["timing"].append(timing)

    # Duration Pattern (Example: 5 Days, 2 Weeks)
    duration_pattern = r"\b\d+\s*(Day|Days|Week|Weeks|Month|Months)\b"

    for match in re.finditer(duration_pattern, text, re.IGNORECASE):
        result["duration"].append(match.group())

    return result