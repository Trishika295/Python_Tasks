import { useState } from "react";


function SearchStudent({ onSearch }) {

    const [search, setSearch] = useState("");


    const handleSearch = () => {

        onSearch(search.trim());

    };


    const handleClear = () => {

        setSearch("");

        onSearch("");

    };


    return (

        <section className="search-section">

            <div className="section-heading">

                <p className="section-label">
                    SEARCH
                </p>

                <h2>
                    Find a Student
                </h2>

            </div>


            <div className="search-box">

                <input
                    type="text"
                    placeholder="Search student by name..."
                    value={search}
                    onChange={(event) =>
                        setSearch(
                            event.target.value
                        )
                    }
                    onKeyDown={(event) => {

                        if (event.key === "Enter") {

                            handleSearch();

                        }

                    }}
                />


                <button
                    className="primary-button"
                    onClick={handleSearch}
                >
                    Search
                </button>


                {search && (

                    <button
                        className="secondary-button"
                        onClick={handleClear}
                    >
                        Clear
                    </button>

                )}

            </div>

        </section>
    );
}


export default SearchStudent;