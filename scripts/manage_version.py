import toml
import argparse


def manage_version():
    with open("pyproject.toml", "r") as f:
        current_pyproject = toml.loads(f.read())

    parser = argparse.ArgumentParser()
    parser.add_argument("--major", action="store_true")
    parser.add_argument("--minor", action="store_true")
    parser.add_argument("--patch", action="store_true")
    parser.add_argument("--dev", action="store_true")
    args = parser.parse_args()

    current_version_parts = current_pyproject["tool"]["poetry"]["version"].split(".")
    if args.major:
        current_version_parts[0] = str(int(current_version_parts[0]) + 1)
        if len(current_version_parts) == 4:
            current_version_parts = current_version_parts[0:3]
    elif args.minor:
        current_version_parts[1] = str(int(current_version_parts[1]) + 1)
    elif args.patch:
        current_version_parts[2] = str(int(current_version_parts[2]) + 1)
    elif args.dev:
        if len(current_version_parts) == 4:
            current_version_parts[3] = str(int(current_version_parts[3]) + 1)
        else:
            current_version_parts.append("0")

    with open("pyproject.toml", "w") as f:
        current_pyproject["tool"]["poetry"]["version"] = ".".join(current_version_parts)
        toml.dump(current_pyproject, f)

    print(f"Updated pyproject.toml version to {'.'.join(current_version_parts)}")
