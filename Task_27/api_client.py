import requests
import sys

API_URL = "https://jsonplaceholder.typicode.com/posts"
TIMEOUT = 10


def fetch_posts(limit=5):
    """Fetch posts from a public REST API."""
    try:
        print("\nConnecting to the public API...")

        response = requests.get(
            API_URL,
            params={"_limit": limit},
            timeout=TIMEOUT
        )

        # Check the HTTP response status
        response.raise_for_status()

        # Convert the JSON response into Python objects
        data = response.json()

        if not isinstance(data, list):
            print("Error: Unexpected API response format.")
            return

        if not data:
            print("No posts were returned by the API.")
            return

        print("\n" + "=" * 60)
        print("          SIMPLE PYTHON API CLIENT")
        print("=" * 60)
        print(f"HTTP Status Code : {response.status_code}")
        print(f"Posts Retrieved  : {len(data)}")
        print("-" * 60)

        # Display selected fields from each JSON object
        for post in data:
            print(f"Post ID : {post.get('id', 'N/A')}")
            print(f"User ID : {post.get('userId', 'N/A')}")
            print(f"Title   : {post.get('title', 'N/A')}")
            print(f"Body    : {post.get('body', 'N/A')}")
            print("-" * 60)

        print("API data retrieved successfully.")

    except requests.exceptions.Timeout:
        print("Error: The API request timed out.")

    except requests.exceptions.ConnectionError:
        print("Error: Unable to connect to the API.")
        print("Check your internet connection and try again.")

    except requests.exceptions.HTTPError as error:
        status = error.response.status_code if error.response is not None else "Unknown"
        print(f"HTTP Error: {status}")
        print("The server could not complete the request.")

    except requests.exceptions.RequestException as error:
        print(f"Request failed: {error}")

    except ValueError:
        print("Error: The API returned invalid JSON data.")

    except KeyboardInterrupt:
        print("\nRequest interrupted by the user.")


def main():
    """Run the API client."""
    print("=" * 60)
    print("             PYTHON REST API CLIENT")
    print("=" * 60)
    print("1. Fetch 5 posts")
    print("2. Fetch 10 posts")
    print("3. Fetch a custom number of posts")
    print("4. Exit")

    try:
        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            fetch_posts(5)
        elif choice == "2":
            fetch_posts(10)
        elif choice == "3":
            limit_text = input("Enter the number of posts (1-100): ").strip()

            try:
                limit = int(limit_text)
                if 1 <= limit <= 100:
                    fetch_posts(limit)
                else:
                    print("Please enter a number between 1 and 100.")
            except ValueError:
                print("Invalid input. Please enter a whole number.")
        elif choice == "4":
            print("Exiting API Client. Goodbye!")
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")

    except (EOFError, KeyboardInterrupt):
        print("\nProgram closed safely.")


if __name__ == "__main__":
    main()
