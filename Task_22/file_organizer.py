from pathlib import Path
import shutil


# File extensions mapped to category folders
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
    "Spreadsheets": [".csv", ".xls", ".xlsx", ".ods"],
    "Presentations": [".ppt", ".pptx", ".odp"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".webm"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Python": [".py", ".pyw"],
    "Code": [".html", ".css", ".js", ".jsx", ".java",
             ".c", ".cpp", ".h", ".php", ".json", ".xml"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
}


def get_category(file_path):
    """Return the category folder for a file."""
    extension = file_path.suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"


def get_unique_path(destination):
    """Generate a unique filename without overwriting existing files."""
    if not destination.exists():
        return destination

    parent = destination.parent
    stem = destination.stem
    suffix = destination.suffix
    counter = 1

    while True:
        new_path = parent / f"{stem}_{counter}{suffix}"

        if not new_path.exists():
            return new_path

        counter += 1


def organize_files(source_folder, destination_folder, preview=True):
    """Organize files by extension, with an optional preview."""
    source = Path(source_folder).expanduser().resolve()
    destination = Path(destination_folder).expanduser().resolve()

    if not source.exists() or not source.is_dir():
        print("Error: Source folder does not exist.")
        return

    if source == destination or source in destination.parents:
        print("Error: Destination must not be inside the source folder.")
        return

    if destination in source.parents:
        print("Error: Destination cannot be a parent of the source folder.")
        return

    # Only inspect files directly inside the source folder.
    files = sorted(
        (item for item in source.iterdir() if item.is_file()),
        key=lambda item: item.name.lower()
    )

    if not files:
        print("No files found in the source folder.")
        return

    print(f"\nSource: {source}")
    print(f"Destination: {destination}")
    print(f"Files found: {len(files)}")
    print("-" * 55)

    moved_count = 0
    skipped_count = 0

    for file_path in files:
        category = get_category(file_path)
        target_folder = destination / category
        target_path = get_unique_path(target_folder / file_path.name)

        if preview:
            print(f"[PREVIEW] {file_path.name} -> {category}/{target_path.name}")
            continue

        try:
            target_folder.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file_path), str(target_path))
            print(f"[MOVED] {file_path.name} -> {category}/{target_path.name}")
            moved_count += 1

        except (OSError, shutil.Error) as error:
            print(f"[ERROR] Could not move {file_path.name}: {error}")
            skipped_count += 1

    print("-" * 55)

    if preview:
        print("Preview completed. No files were moved.")
        print("Run the organizer again and select actual organization to proceed.")
    else:
        print(f"Successfully organized: {moved_count} file(s)")
        print(f"Skipped due to errors: {skipped_count} file(s)")


def main():
    """Display the menu and run the file organizer."""
    print("=" * 45)
    print("       PYTHON FILE ORGANIZER")
    print("=" * 45)

    source = input("Enter the source folder path: ").strip().strip('"')
    destination = input("Enter the destination folder path: ").strip().strip('"')

    print("\n1. Preview organization")
    print("2. Organize files")
    choice = input("Choose an option (1 or 2): ").strip()

    if choice == "1":
        organize_files(source, destination, preview=True)
    elif choice == "2":
        confirmation = input(
            "This will move files from the source folder. Continue? (yes/no): "
        ).strip().lower()

        if confirmation == "yes":
            organize_files(source, destination, preview=False)
        else:
            print("Operation cancelled. No files were moved.")
    else:
        print("Invalid choice. Please select 1 or 2.")


if __name__ == "__main__":
    main()