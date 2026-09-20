import json
from pathlib import Path


# Find the root folder of the project
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Input files
CAMEROON_FILE = PROJECT_ROOT / "data" / "cameroon_projects_2023.json"
KENYA_FILE = PROJECT_ROOT / "data" / "kenya_projects_2023_2026.json"

# Output file
OUTPUT_FILE = PROJECT_ROOT / "data" / "real_projects_2023_2026.json"


def load_json(file_path):
    """Load projects from a JSON file."""
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(f"{file_path.name} must contain a JSON list.")

    return data


def main():
    print("Africa Impact Platform - Combining Project Data")
    print("-" * 55)

    # Load both datasets
    cameroon_projects = load_json(CAMEROON_FILE)
    kenya_projects = load_json(KENYA_FILE)

    print(f"Cameroon projects: {len(cameroon_projects)}")
    print(f"Kenya projects:    {len(kenya_projects)}")

    # Combine the datasets
    all_projects = cameroon_projects + kenya_projects

    print(f"Total projects:    {len(all_projects)}")

    # Save combined dataset
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(all_projects, file, indent=4, ensure_ascii=False)

    print()
    print(f"Combined dataset saved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()

