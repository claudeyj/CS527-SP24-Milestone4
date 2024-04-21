import argparse
from pathlib import Path
from enum import Enum

def is_number(s: str):
    try:
        float(s)
        return True
    except ValueError:
        return False

class Dataset(Enum):
    DEFECTS4J = "Defects4J"
    QUIXBUGS = "QuixBugs"
    BEARS = "Bears"
    BUGSWARM = "BugSwarm"

def validate(repo_path: Path):
    validation_pass = True
    report_path = repo_path / "BL-Results.csv"
    if not report_path.exists():
        validation_pass = False
        print("[FAIL] No BL-Results.csv file")
        return
    with open(report_path) as file:
        lines = file.readlines()
        if len(lines) < 2:
            validation_pass = False
            print("[FAIL] BL-Results.csv is empty")
            return
    head = lines[0].strip().split(",")
    if len(head) != 4:
        validation_pass = False
        print("[FAIL] BL-Results.csv header is invalid, should contain dataset name, bug id, AR, FR")
        return
    
    for line in lines[1:]:
        if line.strip() == "":
            continue
        fields = line.strip().split(",")
        if len(fields) != 4:
            validation_pass = False
            print("[FAIL] BL-Results.csv line is invalid, should contain dataset name, bug id, AR, FR")
            return
        dataset, bug_id, ar, fr = fields
        if dataset not in [dataset.value for dataset in Dataset]:
            validation_pass = False
            print(f"[FAIL] Invalid dataset name: {dataset} for bug {bug_id}")
        bug_dir = repo_path / dataset / bug_id
        if not bug_dir.exists():
            validation_pass = False
            print(f"[FAIL] No bug folder: {bug_dir} for bug {bug_id}")
        if not is_number(ar):
            validation_pass = False
            print(f"[FAIL] Invalid AR: {ar} for bug {bug_id}")
        if not fr.isdigit():
            validation_pass = False
            print(f"[FAIL] Invalid FR: {fr} for bug {bug_id}")

    if validation_pass:
        print("[PASS] Validation successful")

def main():
    parser = argparse.ArgumentParser(description="Validate repository structure for bug datasets.")
    parser.add_argument("repo_path", type=str, help="Path to the repository")
    args = parser.parse_args()

    validate(Path(args.repo_path))

if __name__ == '__main__':
    main()
