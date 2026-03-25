import subprocess
import json
import os


def get_installed_packages():
    try:
        output = subprocess.check_output(["pip", "freeze"], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"Error running pip freeze : {e}")
        return []
    lines = output.decode().splitlines()
    packages = []
    for line in lines:
        if not line.strip():
            continue
        if "==" in line:
            name = line.split("==")[0]
        elif " @ " in line:
            name = line.split(" @ ")[0]
        else:
            name = line.strip()
        packages.append(name)
    return sorted(set(packages))


def show_package_info(name):
    try:
        output = subprocess.check_output(
            ["pip", "show", name], stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError:
        return {"requires": [], "required_by": []}
    text = output.decode()
    requires = []
    required_by = []
    for line in text.splitlines():
        if line.startswith("Requires:"):
            reqs = line.split("Requires:", 1)[1].strip()
            requires = [r.strip() for r in reqs.split(",") if r.strip()]
        elif line.startswith("Required-by:"):
            rby = line.split("Required-by:", 1)[1].strip()
            required_by = [r.strip() for r in rby.split(",") if r.strip()]
    return {"requires": requires, "required_by": required_by}


def build_dependency_map(packages):
    total = len(packages)
    dep_map = {}
    for idx, pkg in enumerate(packages, start=1):
        print(f"Processing [{idx:03}/{total:03}] {pkg}...")
        info = show_package_info(pkg)
        dep_map[pkg] = info
    return dep_map


def write_json(dep_map, filename="dependencies.json"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(dep_map, f, indent=2, ensure_ascii=False)
    print(f"\nWritten dependency JSON to {filename}")


if __name__ == "__main__":
    pkgs = get_installed_packages()
    total = len(pkgs)
    print(f"Found {total} packages to process\n")
    dep_map = build_dependency_map(pkgs)
    write_json(dep_map, os.path.join("output", "dependencies.json"))
