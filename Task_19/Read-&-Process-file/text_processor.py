import os


def validate_file(file_path):
    """
    Validate the input text file.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if not os.path.isfile(file_path):
        raise ValueError(
            "The given path is not a valid file."
        )

    if not file_path.lower().endswith(".txt"):
        raise ValueError(
            "Only .txt files are supported."
        )


def process_text_file(file_path):
    """
    Read a text file and generate text statistics.

    The file is processed line by line so that large files
    do not need to be loaded completely into memory.
    """

    validate_file(file_path)

    line_count = 0
    word_count = 0
    character_count = 0
    characters_without_spaces = 0

    try:
        # Using with open() automatically closes the file.
        with open(file_path, "r", encoding="utf-8") as file:

            # Process the file line by line.
            for line in file:

                line_count += 1

                # Count words
                words = line.split()
                word_count += len(words)

                # Count all characters
                character_count += len(line)

                # Count characters excluding spaces,
                # tabs and newline characters.
                characters_without_spaces += len(
                    line.replace(" ", "")
                        .replace("\t", "")
                        .replace("\n", "")
                        .replace("\r", "")
                )

        # Get file size in bytes
        file_size = os.path.getsize(file_path)

        return {
            "lines": line_count,
            "words": word_count,
            "characters": character_count,
            "characters_without_spaces": characters_without_spaces,
            "file_size": file_size
        }

    except UnicodeDecodeError:
        raise ValueError(
            "The file could not be read as UTF-8 text."
        )

    except PermissionError:
        raise PermissionError(
            "Permission denied while accessing the file."
        )


def read_text_file(file_path):
    """
    Read the complete text file.
    """

    validate_file(file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    except UnicodeDecodeError:
        raise ValueError(
            "The file could not be read as UTF-8 text."
        )

    except PermissionError:
        raise PermissionError(
            "Permission denied while accessing the file."
        )


def read_text_preview(file_path, max_characters=2000):
    """
    Read only a limited number of characters for preview.
    """

    validate_file(file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read(max_characters)

    except UnicodeDecodeError:
        raise ValueError(
            "The file could not be read as UTF-8 text."
        )

    except PermissionError:
        raise PermissionError(
            "Permission denied while accessing the file."
        )


def calculate_text_statistics(text):
    """
    Calculate statistics directly from text content.

    This function is useful for uploaded files in Streamlit.
    """

    lines = text.splitlines()

    line_count = len(lines)

    word_count = len(text.split())

    character_count = len(text)

    characters_without_spaces = len(
        text.replace(" ", "")
            .replace("\t", "")
            .replace("\n", "")
            .replace("\r", "")
    )

    return {
        "lines": line_count,
        "words": word_count,
        "characters": character_count,
        "characters_without_spaces": characters_without_spaces
    }


def format_file_size(size_in_bytes):
    """
    Convert file size into a readable format.
    """

    if size_in_bytes < 1024:
        return f"{size_in_bytes} Bytes"

    elif size_in_bytes < 1024 * 1024:
        return f"{size_in_bytes / 1024:.2f} KB"

    elif size_in_bytes < 1024 * 1024 * 1024:
        return f"{size_in_bytes / (1024 * 1024):.2f} MB"

    else:
        return f"{size_in_bytes / (1024 * 1024 * 1024):.2f} GB"