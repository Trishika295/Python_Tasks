import sys
import os
import subprocess
import tempfile

import streamlit as st

from text_processor import process_text_file
from text_processor import read_text_file
from text_processor import read_text_preview
from text_processor import calculate_text_statistics
from text_processor import format_file_size

# TERMINAL FUNCTIONS

def print_statistics(statistics, file_name):
    """
    Display file statistics in the terminal.
    """

    print("\n" + "=" * 55)
    print("              TEXT FILE STATISTICS")
    print("=" * 55)

    print(f"File Name                     : {file_name}")
    print(f"Number of Lines               : {statistics['lines']}")
    print(f"Number of Words               : {statistics['words']}")
    print(f"Number of Characters         : {statistics['characters']}")
    print(
        "Characters Without Spaces    : "
        f"{statistics['characters_without_spaces']}"
    )

    if "file_size" in statistics:
        print(
            "File Size                     : "
            f"{format_file_size(statistics['file_size'])}"
        )

    print("=" * 55)


def terminal_mode():
    """
    Run the application in terminal/CMD mode.
    """

    print("\n" + "=" * 55)
    print("          READ AND PROCESS A TEXT FILE")
    print("=" * 55)

    print("\nThis program reads a .txt file and generates")
    print("line, word and character statistics.")

    print("\nEnter the path of the text file.")
    print("Example: sample.txt")

    file_path = input("\nEnter file path: ").strip()

    if not file_path:
        print("\nError: File path cannot be empty.")
        return

    try:
        statistics = process_text_file(file_path)

        file_name = os.path.basename(file_path)

        print_statistics(statistics, file_name)

        print("\nText Preview")
        print("-" * 55)

        preview = read_text_preview(
            file_path,
            max_characters=500
        )

        if preview.strip():
            print(preview)

            if len(preview) >= 500:
                print("\n[Preview limited to first 500 characters]")
        else:
            print("[The file is empty.]")

        print("-" * 55)

    except FileNotFoundError as error:
        print(f"\nError: {error}")

    except PermissionError as error:
        print(f"\nError: {error}")

    except ValueError as error:
        print(f"\nError: {error}")

    except Exception as error:
        print(f"\nUnexpected error: {error}")

# BROWSER MODE

def browser_mode():
    """
    Start the Streamlit application.
    """

    print("\nStarting Streamlit browser application...")

    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                os.path.abspath(__file__)
            ]
        )

    except FileNotFoundError:
        print(
            "\nStreamlit is not installed."
            "\nInstall it using:"
            "\npython -m pip install streamlit"
        )


# ==========================================================
# BOTH MODES
# ==========================================================

def both_mode():
    """
    Start Streamlit in the browser and then allow
    the user to process a file through the terminal.
    """

    print("\nStarting browser application...")

    try:

        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                os.path.abspath(__file__)
            ]
        )

        print("\nStreamlit has been started.")
        print("The browser should open automatically.")
        print("\nTerminal mode is also available below.")

        terminal_mode()

        print("\nStopping browser application...")

        process.terminate()

    except FileNotFoundError:
        print(
            "\nStreamlit is not installed."
            "\nInstall it using:"
            "\npython -m pip install streamlit"
        )


# ==========================================================
# STREAMLIT FRONTEND
# ==========================================================

def streamlit_app():

    # ------------------------------------------------------
    # Page Configuration
    # ------------------------------------------------------

    st.set_page_config(
        page_title="Read and Process a Text File",
        page_icon="",
        layout="wide"
    )

    # ------------------------------------------------------
    # Custom CSS
    # ------------------------------------------------------

    st.markdown(
        """
        <style>

        .main-title {
            text-align: center;
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .subtitle {
            text-align: center;
            font-size: 17px;
            margin-bottom: 30px;
        }

        .info-box {
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    # ------------------------------------------------------
    # Header
    # ------------------------------------------------------

    st.markdown(
        '<div class="main-title">'
        ' Read and Process a Text File'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Upload a text file and generate useful text statistics.'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    # ------------------------------------------------------
    # File Upload
    # ------------------------------------------------------

    uploaded_file = st.file_uploader(
        "Choose a text file",
        type=["txt"],
        help="Only .txt files are supported."
    )

    if uploaded_file is None:

        st.info(
            "Please upload a .txt file to start processing."
        )

        st.subheader("Project Features")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(" **Line Count**")
            st.write(
                "Calculate the total number of lines "
                "in the text file."
            )

        with col2:
            st.write(" **Word Count**")
            st.write(
                "Calculate the total number of words "
                "using Python text processing."
            )

        with col3:
            st.write(" **Character Count**")
            st.write(
                "Calculate total characters with and "
                "without spaces."
            )

        return

    # ------------------------------------------------------
    # Process Uploaded File
    # ------------------------------------------------------

    st.success(
        f"Successfully uploaded: {uploaded_file.name}"
    )

    try:

        # Get uploaded file content
        file_bytes = uploaded_file.getvalue()

        # Decode text
        text = file_bytes.decode("utf-8")

        # Calculate statistics using backend function
        statistics = calculate_text_statistics(text)

        # File size
        file_size = len(file_bytes)

        # --------------------------------------------------
        # Statistics
        # --------------------------------------------------

        st.subheader("Generated Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Lines",
                statistics["lines"]
            )

        with col2:
            st.metric(
                "Words",
                statistics["words"]
            )

        with col3:
            st.metric(
                "Characters",
                statistics["characters"]
            )

        with col4:
            st.metric(
                "Characters Without Spaces",
                statistics["characters_without_spaces"]
            )

        # --------------------------------------------------
        # File Information
        # --------------------------------------------------

        st.subheader("File Information")

        info_col1, info_col2 = st.columns(2)

        with info_col1:
            st.write(
                f"**File Name:** {uploaded_file.name}"
            )

        with info_col2:
            st.write(
                f"**File Size:** {format_file_size(file_size)}"
            )

        # --------------------------------------------------
        # Text Preview
        # --------------------------------------------------

        st.subheader("Text Preview")

        preview = text[:2000]

        if preview.strip():

            st.text_area(
                "First 2000 characters",
                preview,
                height=300
            )

            if len(text) > 2000:
                st.caption(
                    "Preview limited to the first "
                    "2000 characters."
                )

        else:

            st.warning(
                "The uploaded file is empty."
            )

        # --------------------------------------------------
        # Processing Details
        # --------------------------------------------------

        st.subheader("Processing Details")

        st.write(
            "The file was processed using Python file "
            "handling and text-processing functions."
        )

        st.write(
            "The backend calculates line, word and "
            "character statistics."
        )

        st.write(
            "The application supports UTF-8 encoded "
            "text files."
        )

    except UnicodeDecodeError:

        st.error(
            "Unable to process the file. "
            "Please upload a valid UTF-8 text file."
        )

    except Exception as error:

        st.error(
            f"An error occurred while processing the file: "
            f"{error}"
        )

    # ------------------------------------------------------
    # Footer
    # ------------------------------------------------------

    st.divider()

    st.caption(
        "Task 19 | Read and Process a Text File | "
        "Python + Streamlit"
    )


# ==========================================================
# PROGRAM ENTRY POINT
# ==========================================================

def main():

    # ------------------------------------------------------
    # Terminal arguments
    # ------------------------------------------------------

    if len(sys.argv) > 1:

        mode = sys.argv[1].lower()

        if mode == "--terminal":
            terminal_mode()
            return

        elif mode == "--browser":
            browser_mode()
            return

        elif mode == "--both":
            both_mode()
            return

        elif mode in ["--help", "-h"]:

            print("\nUsage:")
            print(
                "python app.py --terminal"
                "  -> Run terminal version"
            )
            print(
                "python app.py --browser"
                "   -> Open browser version"
            )
            print(
                "python app.py --both"
                "      -> Run terminal + browser"
            )

            return

    # ------------------------------------------------------
    # Streamlit execution
    # ------------------------------------------------------

    streamlit_app()


if __name__ == "__main__":
    main()