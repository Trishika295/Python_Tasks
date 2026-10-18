
import csv
from io import StringIO

import pandas as pd
import requests
import streamlit as st

from web_scraper import (
    BASE_URL,
    scrape_website,
    save_to_csv,
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="BookScope | Web Scraper",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ==================================================
# CATALOG DROPDOWN
# ==================================================

WEBSITE_OPTIONS = {
    "Main Catalog": "https://books.toscrape.com/",
    "Catalog Page 2": "https://books.toscrape.com/catalogue/page-2.html",
    "Catalog Page 3": "https://books.toscrape.com/catalogue/page-3.html",
    "Catalog Page 4": "https://books.toscrape.com/catalogue/page-4.html",
    "Catalog Page 5": "https://books.toscrape.com/catalogue/page-5.html",
    "Catalog Page 6": "https://books.toscrape.com/catalogue/page-6.html",
    "Catalog Page 7": "https://books.toscrape.com/catalogue/page-7.html",
    "Catalog Page 8": "https://books.toscrape.com/catalogue/page-8.html",
    "Catalog Page 9": "https://books.toscrape.com/catalogue/page-9.html",
    "Catalog Page 10": "https://books.toscrape.com/catalogue/page-10.html",
}


def update_selected_url():
    st.session_state["scraper_url"] = WEBSITE_OPTIONS[
        st.session_state["website_choice"]
    ]


if "website_choice" not in st.session_state:
    st.session_state["website_choice"] = "Main Catalog"

if "scraper_url" not in st.session_state:
    st.session_state["scraper_url"] = BASE_URL


if "bookscope_records" not in st.session_state:
    st.session_state["bookscope_records"] = []


# ==================================================
# PROFESSIONAL CSS
# ==================================================

st.markdown(
    """
    <style>
    #MainMenu, footer, header {
        visibility: hidden;
    }

    [data-testid="stSidebar"] {
        display: none;
    }

    .block-container {
        max-width: 1450px;
        padding: 2rem 3rem 3rem;
    }

    .hero {
        background: linear-gradient(120deg, #eee7ff, #fff1f6);
        border: 1px solid #e6daf8;
        border-radius: 22px;
        padding: 32px;
        margin-bottom: 25px;
    }

    .eyebrow {
        color: #7553a6;
        font-size: 12px;
        letter-spacing: 2px;
        font-weight: 700;
    }

    .hero h1 {
        color: #302044;
        font-size: 40px;
        margin: 8px 0;
    }

    .hero p {
        color: #625873;
        font-size: 16px;
        margin-bottom: 0;
    }

    .section-title {
        color: #302640;
        font-size: 24px;
        font-weight: 700;
        margin: 24px 0 14px;
    }

    div.stButton > button {
        background: #6741a5;
        color: white;
        border: 1px solid #6741a5;
        border-radius: 10px;
        min-height: 46px;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background: #503080;
        border-color: #503080;
        color: white;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e9e4ef;
        padding: 16px;
        border-radius: 14px;
    }

    .footer-text {
        color: #81788b;
        font-size: 12px;
        text-align: center;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }

        .hero {
            padding: 22px;
        }

        .hero h1 {
            font-size: 30px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# HEADER
# ==================================================

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">PYTHON DATA EXTRACTION WORKSPACE</div>
        <h1>🔎 BookScope</h1>
        <p>
            Discover book details, explore catalog data,
            and export your collected records with ease.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==================================================
# SCRAPER CONFIGURATION
# ==================================================

st.markdown(
    '<div class="section-title">1. Configure your scrape</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):

    st.selectbox(
        "Choose a catalog page",
        options=list(WEBSITE_OPTIONS.keys()),
        key="website_choice",
        on_change=update_selected_url,
    )

    url = st.text_input(
        "Website URL",
        key="scraper_url",
        help="Choose a catalog page from the dropdown.",
    )

    col_pages, col_info = st.columns([1, 2])

    with col_pages:
        max_pages = st.number_input(
            "Number of pages to scrape",
            min_value=1,
            max_value=10,
            value=3,
            step=1,
        )

    with col_info:
        st.write("")
        st.caption(
            "Collect records from 1–10 catalog pages. "
            "Requests are spaced apart to reduce server load."
        )

    run_scrape = st.button(
        "🔍 Run Scraper",
        use_container_width=True,
    )


# ==================================================
# SCRAPE BUTTON ACTION
# ==================================================

if run_scrape:

    st.session_state["bookscope_error"] = ""

    progress_bar = st.progress(0)
    status_text = st.empty()

    def update_progress(message, fraction):
        progress_bar.progress(
            min(max(float(fraction), 0.0), 1.0)
        )
        status_text.write(message)

    try:
        with st.spinner("Checking access and collecting data..."):

            records, permission_message, pages_scraped = (
                scrape_website(
                    start_url=url.strip(),
                    max_pages=int(max_pages),
                    progress=update_progress,
                )
            )

        save_to_csv(records)

        st.session_state["bookscope_records"] = records
        st.session_state["bookscope_pages"] = pages_scraped
        st.session_state["bookscope_permission"] = permission_message
        st.session_state["bookscope_source"] = url.strip()

        st.success(
            f"Scraping completed successfully! "
            f"{len(records)} books collected from "
            f"{pages_scraped} page(s)."
        )

        st.info(permission_message)

    except PermissionError as error:
        st.session_state["bookscope_records"] = []
        st.session_state["bookscope_error"] = str(error)

    except requests.Timeout:
        st.session_state["bookscope_error"] = (
            "The request timed out. Please try again."
        )

    except requests.HTTPError as error:
        st.session_state["bookscope_error"] = (
            f"HTTP error: {error}"
        )

    except requests.RequestException as error:
        st.session_state["bookscope_error"] = (
            f"Network error: {error}"
        )

    except (ValueError, OSError, csv.Error) as error:
        st.session_state["bookscope_error"] = str(error)

    finally:
        progress_bar.empty()
        status_text.empty()


# ==================================================
# ERROR MESSAGE
# ==================================================

if st.session_state.get("bookscope_error"):
    st.error(st.session_state["bookscope_error"])


# ==================================================
# RESULTS
# ==================================================

records = st.session_state.get("bookscope_records", [])

if records:

    df = pd.DataFrame(records)

    expected_columns = [
        "title",
        "price",
        "availability",
        "rating",
        "product_url",
        "image_url",
        "page_number",
    ]

    for column in expected_columns:
        if column not in df.columns:
            df[column] = ""

    st.markdown(
        '<div class="section-title">2. Collection overview</div>',
        unsafe_allow_html=True,
    )

    prices = pd.to_numeric(
        df["price"]
        .astype(str)
        .str.replace("£", "", regex=False)
        .str.strip(),
        errors="coerce",
    )

    average_price = (
        f"£{prices.mean():.2f}"
        if prices.notna().any()
        else "N/A"
    )

    rating_counts = df["rating"].value_counts()

    common_rating = (
        rating_counts.index[0]
        if not rating_counts.empty
        else "N/A"
    )

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric("Books collected", len(df))
    metric2.metric(
        "Pages processed",
        st.session_state.get("bookscope_pages", 0),
    )
    metric3.metric("Average listed price", average_price)
    metric4.metric("Most common rating", str(common_rating))

    # ----------------------------------------------
    # SEARCH AND FILTERS
    # ----------------------------------------------

    st.markdown(
        '<div class="section-title">3. Explore the dataset</div>',
        unsafe_allow_html=True,
    )

    col_search, col_rating, col_page = st.columns([2, 1, 1])

    with col_search:
        search_text = st.text_input(
            "Search book titles",
            placeholder="Type a title...",
        )

    with col_rating:
        rating_options = sorted(
            df["rating"].dropna().astype(str).unique().tolist()
        )

        selected_rating = st.selectbox(
            "Rating",
            ["All ratings"] + rating_options,
        )

    with col_page:
        page_options = sorted(
            pd.to_numeric(
                df["page_number"], errors="coerce"
            ).dropna().astype(int).unique().tolist()
        )

        selected_page = st.selectbox(
            "Catalog page",
            ["All pages"] + page_options,
        )

    filtered_df = df.copy()

    if search_text:
        filtered_df = filtered_df[
            filtered_df["title"].astype(str).str.contains(
                search_text,
                case=False,
                na=False,
            )
        ]

    if selected_rating != "All ratings":
        filtered_df = filtered_df[
            filtered_df["rating"].astype(str) == selected_rating
        ]

    if selected_page != "All pages":
        filtered_df = filtered_df[
            pd.to_numeric(
                filtered_df["page_number"], errors="coerce"
            ) == selected_page
        ]

    st.caption(
        f"Showing {len(filtered_df)} of {len(df)} collected books."
    )

    display_df = filtered_df.rename(
        columns={
            "title": "Book title",
            "price": "Price",
            "availability": "Availability",
            "rating": "Rating",
            "product_url": "Product link",
            "image_url": "Image link",
            "page_number": "Catalog page",
        }
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=420,
        column_config={
            "Product link": st.column_config.LinkColumn(
                "Product link",
                display_text="Open book",
            ),
            "Image link": st.column_config.LinkColumn(
                "Image link",
                display_text="Open image",
            ),
        },
    )

    # ----------------------------------------------
    # BOOK PREVIEW CARDS
    # ----------------------------------------------

    st.markdown(
        '<div class="section-title">4. Book previews</div>',
        unsafe_allow_html=True,
    )

    if filtered_df.empty:
        st.warning("No books match the selected filters.")

    else:
        preview_columns = st.columns(3)

        for index, (_, book) in enumerate(
            filtered_df.head(6).iterrows()
        ):

            with preview_columns[index % 3]:

                with st.container(border=True):

                    image_url = str(book["image_url"])

                    if image_url.startswith("https://"):
                        st.image(image_url, width=115)

                    st.markdown(f"**{book['title']}**")
                    st.write(f"**Price:** {book['price']}")
                    st.write(
                        f"**Rating:** {book['rating'] or 'N/A'}"
                    )
                    st.caption(str(book["availability"]))

                    product_url = str(book["product_url"])

                    if product_url.startswith("https://"):
                        st.link_button(
                            "View book",
                            product_url,
                            use_container_width=True,
                        )

    # ----------------------------------------------
    # CSV DOWNLOAD
    # ----------------------------------------------

    st.markdown(
        '<div class="section-title">5. Export dataset</div>',
        unsafe_allow_html=True,
    )

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    st.download_button(
        label="⬇ Download complete CSV",
        data="\ufeff" + csv_buffer.getvalue(),
        file_name="scraped_data.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.caption(
        "The download includes all collected books, "
        "not just the records currently visible after filtering."
    )


# ==================================================
# EMPTY STATE
# ==================================================

else:

    st.markdown(
        '<div class="section-title">How it works</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.markdown("### 01 · Select")
            st.write(
                "Choose a catalog page and select the number "
                "of pages to process."
            )

    with col2:
        with st.container(border=True):
            st.markdown("### 02 · Explore")
            st.write(
                "View book titles, prices, ratings, availability "
                "and product links."
            )

    with col3:
        with st.container(border=True):
            st.markdown("### 03 · Export")
            st.write(
                "Filter the collected records and download "
                "the complete CSV dataset."
            )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.markdown(
    """
    <div class="footer-text">
        BookScope · Python Web Scraping Mini Project
        <br>
        Educational practice website only.
        Respect website terms and automated-access restrictions.
    </div>
    """,
    unsafe_allow_html=True,
)
