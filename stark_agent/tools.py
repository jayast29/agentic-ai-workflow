FAKE_AVAILABILITY = {
    "2026-01-09": "Busy all day",
    "2026-01-10": "Available from 11:00 AM to 03:00 PM",
    "2026-01-11": "Available from 11:00 AM to 03:00 PM",
    "2026-01-13": "Available all day",
    "2026-01-14": "Busy all day",
}

def get_availability(date_str: str) -> dict[str, str]:
    """
    Simulates checking Stark's availability on a specific date.

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
            "message": f"On {date_str}, Stark is {availability}.",
        }

    return {
        "status": "input_required",
        "message": f"He is not available on {date_str}. Please ask about another date.",
    }

from crewai.tools import BaseTool


class AvailabilityTool(BaseTool):
    name: str = "Calendar Availability Checker"
    description: str = "Checks Stark's availability for a given date."

    def _run(self, date: str) -> str:
        return get_availability(date)["message"]