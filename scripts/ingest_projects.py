import json
from pathlib import Path

import requests


API_URL = "http://127.0.0.1:8000/api/projects/bulk/"
DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "sample_projects.json"


def load_projects():
    """Load project data from the JSON file."""

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        projects = json.load(file)

    if not isinstance(projects, list):
        raise ValueError("Project data must be a JSON list.")

    return projects


def validate_projects(projects):
    """Perform basic validation before sending data to the API."""

    required_fields = [
        "name",
        "description",
        "country",
        "location",
        "impact_area",
        "status",
        "start_date",
    ]

    valid_projects = []

    for index, project in enumerate(projects, start=1):

        missing_fields = [
            field
            for field in required_fields
            if not project.get(field)
        ]

        if missing_fields:
            print(
                f"Skipping project {index}: "
                f"missing {', '.join(missing_fields)}"
            )
            continue

        # Enforce our 2023+ dataset rule
        start_year = int(project["start_date"][:4])

        if start_year < 2023:
            print(
                f"Skipping project {index}: "
                f"start year {start_year} is before 2023."
            )
            continue

        valid_projects.append(project)

    return valid_projects


def send_to_api(projects):
    """Send validated projects to the Django bulk API."""

    response = requests.post(
        API_URL,
        json=projects,
        timeout=30,
    )

    if response.status_code == 201:
        return response.json()

    print(f"API request failed: {response.status_code}")
    print(response.text)

    return None


def main():
    print("Africa Impact Platform - Project Ingestion")
    print("-" * 50)

    try:
        projects = load_projects()

        print(f"Loaded {len(projects)} projects.")

        valid_projects = validate_projects(projects)

        print(
            f"Validated {len(valid_projects)} projects."
        )

        if not valid_projects:
            print("No valid projects to import.")
            return

        result = send_to_api(valid_projects)

        if result:
            print()
            print(result["message"])

    except FileNotFoundError:
        print(f"Data file not found: {DATA_FILE}")

    except json.JSONDecodeError:
        print("Invalid JSON file.")

    except requests.exceptions.ConnectionError:
        print(
            "Could not connect to the Django API.\n"
            "Make sure the Django development server is running."
        )

    except Exception as error:
        print(f"Unexpected error: {error}")


if __name__ == "__main__":
    main()