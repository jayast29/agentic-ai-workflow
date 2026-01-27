FAKE_AVAILABILITY = {
    "2026-01-09": "Available from 4:00 PM to 6:00 PM",
    "2026-01-10": "Available from 10:00 AM to 12:00 PM",
    "2026-01-11": "Available from 11:00 AM to 12:00 PM",
    "2026-01-12": "Busy all afternoon (1:00 PM – 5:00 PM)",
    "2026-01-13": "Available all day",
}

def get_availability(date_str: str) -> dict[str, str]:
    """
    Simulates checking Thor's availability on a specific date.

    Args:
        date_str (str): A date in 'YYYY-MM-DD' format.

    Returns:
        dict: A small JSON-like dictionary with availability info.
    """

    if not date_str:
        return {"status": "error", "message": "No date provided."}

    availability = FAKE_AVAILABILITY.get(date_str)

    if availability:
        return {
            "status": "completed",
            "message": f"On {date_str}, Thor is {availability}.",
        }

    return {
        "status": "input_required",
        "message": f"He is not available on {date_str}. Please ask about another date.",
    }