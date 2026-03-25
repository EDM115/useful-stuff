import json


def load_dependencies(path="output/dependencies.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def summarize(dep_map):
    # 1) Packages required by no-one
    no_dependents = [
        pkg for pkg, info in dep_map.items() if not info.get("required_by")
    ]

    # 2) Most required-by packages
    max_dependents = 0
    most_required_by = []
    for pkg, info in dep_map.items():
        count = len(info.get("required_by", []))
        if count > max_dependents:
            max_dependents = count
            most_required_by = [pkg]
        elif count == max_dependents:
            most_required_by.append(pkg)

    # 3) Packages with the most requires
    max_requires = 0
    most_requires = []
    for pkg, info in dep_map.items():
        count = len(info.get("requires", []))
        if count > max_requires:
            max_requires = count
            most_requires = [pkg]
        elif count == max_requires:
            most_requires.append(pkg)

    # Print results
    print("Packages required by no other package:")
    for pkg in sorted(no_dependents):
        print(f"  - {pkg}")
    print()

    print(f"Package(s) with the most dependents ({max_dependents}):")
    for pkg in sorted(most_required_by):
        print(f"  - {pkg}")
    print()

    print(f"Package(s) with the most direct dependencies ({max_requires}):")
    for pkg in sorted(most_requires):
        print(f"  - {pkg}")
    print()


def main():
    dep_map = load_dependencies()
    summarize(dep_map)


if __name__ == "__main__":
    main()
