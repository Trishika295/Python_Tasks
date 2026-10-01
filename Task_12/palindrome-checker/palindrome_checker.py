def normalize_text(text):
    """
    Normalize the input by:
    - Converting all characters to lowercase
    - Removing spaces
    """
    return text.lower().replace(" ", "")


def check_palindrome(text):
    """
    Check whether the given text is a palindrome.
    """
    normalized_text = normalize_text(text)
    reversed_text = normalized_text[::-1]

    return normalized_text == reversed_text, normalized_text, reversed_text


def main():
    print("=" * 50)
    print("           PALINDROME CHECKER")
    print("=" * 50)

    text = input("\nEnter a word or sentence: ").strip()

    if not text:
        print("\nError: Please enter a word or sentence.")
        return

    is_palindrome, normalized_text, reversed_text = check_palindrome(text)

    print("\n" + "-" * 50)
    print("Original Text  :", text)
    print("Normalized Text:", normalized_text)
    print("Reversed Text  :", reversed_text)
    print("-" * 50)

    if is_palindrome:
        print("Result         : It is a Palindrome!")
    else:
        print("Result         : It is NOT a Palindrome.")

    print("-" * 50)


if __name__ == "__main__":
    main()