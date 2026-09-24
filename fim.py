import os
import json
import hashlib


BASELINE_FILE = "baseline.json"


def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            data = file.read(4096)

            if not data:
                break

            sha256.update(data)

    return sha256.hexdigest()


def scan_folder(folder_path):
    file_hashes = {}

    for root, folders, files in os.walk(folder_path):
        for file_name in files:

            if file_name == BASELINE_FILE:
                continue

            file_path = os.path.join(root, file_name)

            try:
                file_hash = calculate_hash(file_path)

                relative_path = os.path.relpath(
                    file_path, folder_path
                )

                file_hashes[relative_path] = file_hash

            except PermissionError:
                print("Permission denied:", file_path)

    return file_hashes


def create_baseline(folder_path):
    print("\nCreating baseline...")

    file_hashes = scan_folder(folder_path)

    with open(BASELINE_FILE, "w") as file:
        json.dump(file_hashes, file, indent=4)

    print("\nBaseline created successfully.")
    print("Files monitored:", len(file_hashes))


def check_integrity(folder_path):
    print("\nChecking file integrity...")

    if not os.path.exists(BASELINE_FILE):
        print("Baseline does not exist.")
        print("Create a baseline first.")
        return

    with open(BASELINE_FILE, "r") as file:
        old_hashes = json.load(file)

    new_hashes = scan_folder(folder_path)

    modified_files = []
    new_files = []
    deleted_files = []

    # Check modified and deleted files
    for file_path in old_hashes:

        if file_path not in new_hashes:
            deleted_files.append(file_path)

        elif old_hashes[file_path] != new_hashes[file_path]:
            modified_files.append(file_path)

    # Check new files
    for file_path in new_hashes:

        if file_path not in old_hashes:
            new_files.append(file_path)

    # Display results

    print("\n========== RESULTS ==========")

    if modified_files:
        print("\nMODIFIED FILES:")
        for file in modified_files:
            print("  [MODIFIED]", file)

    if new_files:
        print("\nNEW FILES:")
        for file in new_files:
            print("  [NEW]", file)

    if deleted_files:
        print("\nDELETED FILES:")
        for file in deleted_files:
            print("  [DELETED]", file)

    if not modified_files and not new_files and not deleted_files:
        print("\nNo changes detected.")

    print("\n=============================")


def main():

    print("==============================")
    print(" FILE INTEGRITY MONITOR")
    print("==============================")

    folder_path = input(
        "\nEnter the folder path to monitor: "
    ).strip()

    if not os.path.exists(folder_path):
        print("\nFolder does not exist.")
        return

    while True:

        print("\nChoose an option:")
        print("1. Create baseline")
        print("2. Check integrity")
        print("3. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            create_baseline(folder_path)

        elif choice == "2":
            check_integrity(folder_path)

        elif choice == "3":
            print("\nExiting...")
            break

        else:
            print("\nInvalid choice.")


if __name__ == "__main__":
    main()