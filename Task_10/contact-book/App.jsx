import React, { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:5000/api/contacts";

function App() {
  const [contacts, setContacts] = useState({});
  const [form, setForm] = useState({
    id: "",
    name: "",
    phone: "",
    email: ""
  });

  const [editingId, setEditingId] = useState(null);
  const [search, setSearch] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  // -----------------------------------------
  // Load contacts
  // -----------------------------------------

  const loadContacts = async () => {
    try {
      setLoading(true);

      const response = await fetch(API_URL);
      const data = await response.json();

      setContacts(data);
      setError("");
    } catch (err) {
      setError(
        "Unable to connect to the Python backend. Make sure Flask is running."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadContacts();
  }, []);

  // -----------------------------------------
  // Handle input
  // -----------------------------------------

  const handleChange = (event) => {
    setForm({
      ...form,
      [event.target.name]: event.target.value
    });

    setMessage("");
    setError("");
  };

  // -----------------------------------------
  // Add / Update
  // -----------------------------------------

  const handleSubmit = async (event) => {
    event.preventDefault();

    setMessage("");
    setError("");

    try {
      let response;

      if (editingId) {
        response = await fetch(`${API_URL}/${editingId}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            name: form.name,
            phone: form.phone,
            email: form.email
          })
        });
      } else {
        response = await fetch(API_URL, {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(form)
        });
      }

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Something went wrong.");
        return;
      }

      setMessage(
        editingId
          ? "Contact updated successfully!"
          : "Contact added successfully!"
      );

      resetForm();
      await loadContacts();
    } catch (err) {
      setError(
        "Unable to connect to the Python backend."
      );
    }
  };

  // -----------------------------------------
  // Edit
  // -----------------------------------------

  const handleEdit = (id) => {
    const contact = contacts[id];

    setForm({
      id: id,
      name: contact.name,
      phone: contact.phone,
      email: contact.email
    });

    setEditingId(id);
    setMessage("");
    setError("");

    window.scrollTo({
      top: 0,
      behavior: "smooth"
    });
  };

  // -----------------------------------------
  // Delete
  // -----------------------------------------

  const handleDelete = async (id) => {
    const contact = contacts[id];

    const confirmDelete = window.confirm(
      `Delete contact "${contact.name}"?`
    );

    if (!confirmDelete) {
      return;
    }

    try {
      const response = await fetch(`${API_URL}/${id}`, {
        method: "DELETE"
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.error || "Unable to delete contact.");
        return;
      }

      setMessage("Contact deleted successfully!");

      await loadContacts();
    } catch (err) {
      setError(
        "Unable to connect to the Python backend."
      );
    }
  };

  // -----------------------------------------
  // Reset form
  // -----------------------------------------

  const resetForm = () => {
    setForm({
      id: "",
      name: "",
      phone: "",
      email: ""
    });

    setEditingId(null);
  };

  // -----------------------------------------
  // Search
  // -----------------------------------------

  const filteredContacts = Object.entries(contacts).filter(
    ([id, contact]) => {
      const searchText = search.toLowerCase().trim();

      return (
        id.toLowerCase().includes(searchText) ||
        contact.name.toLowerCase().includes(searchText) ||
        contact.phone.includes(searchText) ||
        contact.email.toLowerCase().includes(searchText)
      );
    }
  );

  // -----------------------------------------
  // UI
  // -----------------------------------------

  return (
    <div className="app">

      {/* Header */}
      <header className="header">

        <div className="header-content">

          <div>

            <h1>Contact Book</h1>

            <p className="header-description">
              Manage contacts using Python dictionaries
              and CRUD operations.
            </p>
          </div>

          <div className="dictionary-box">
            <span className="dictionary-icon">
              {"{ }"}
            </span>

            <span>
              Dictionary
            </span>
          </div>

        </div>

      </header>


      <main className="container">

        {/* Statistics */}
        <section className="stats">

          <div className="stat-card">
            <span className="stat-number">
              {Object.keys(contacts).length}
            </span>

            <span className="stat-label">
              Total Contacts
            </span>
          </div>

          <div className="stat-card">
            <span className="stat-number">
              CRUD
            </span>

            <span className="stat-label">
              Operations
            </span>
          </div>

          <div className="stat-card">
            <span className="stat-number">
              Python
            </span>

            <span className="stat-label">
              Backend
            </span>
          </div>

          <div className="stat-card">
            <span className="stat-number">
              React
            </span>

            <span className="stat-label">
              Frontend
            </span>
          </div>

        </section>


        {/* Messages */}

        {message && (
          <div className="success-message">
            ✓ {message}
          </div>
        )}

        {error && (
          <div className="error-message">
            ⚠ {error}
          </div>
        )}


        {/* Add / Update Form */}

        <section className="card">

          <div className="section-heading">

            <div>
              <span className="section-tag">
                {editingId ? "UPDATE" : "CREATE"}
              </span>

              <h2>
                {editingId
                  ? "Update Contact"
                  : "Add New Contact"}
              </h2>

              <p>
                {editingId
                  ? "Modify the selected contact information."
                  : "Add a new contact to your dictionary."}
              </p>
            </div>

          </div>


          <form onSubmit={handleSubmit}>

            <div className="form-grid">

              <div className="input-group">

                <label>
                  Contact ID
                </label>

                <input
                  type="text"
                  name="id"
                  placeholder="C004"
                  value={form.id}
                  onChange={handleChange}
                  disabled={editingId !== null}
                  required
                />

                <small>
                  Example: C001
                </small>

              </div>


              <div className="input-group">

                <label>
                  Full Name
                </label>

                <input
                  type="text"
                  name="name"
                  placeholder="Enter full name"
                  value={form.name}
                  onChange={handleChange}
                  required
                />

              </div>


              <div className="input-group">

                <label>
                  Phone Number
                </label>

                <input
                  type="tel"
                  name="phone"
                  placeholder="9876543210"
                  value={form.phone}
                  onChange={handleChange}
                  required
                />

              </div>


              <div className="input-group">

                <label>
                  Email Address
                </label>

                <input
                  type="email"
                  name="email"
                  placeholder="name@gmail.com"
                  value={form.email}
                  onChange={handleChange}
                  required
                />

              </div>

            </div>


            <div className="form-actions">

              <button
                className="primary-btn"
                type="submit"
              >
                {editingId
                  ? "Update Contact"
                  : "Add Contact"}
              </button>


              {editingId && (
                <button
                  className="secondary-btn"
                  type="button"
                  onClick={resetForm}
                >
                  Cancel
                </button>
              )}

            </div>

          </form>

        </section>


        {/* Contacts */}

        <section className="card">

          <div className="list-header">

            <div>
              <span className="section-tag">
                READ
              </span>

              <h2>
                Contact Directory
              </h2>

              <p>
                Search and manage your saved contacts.
              </p>
            </div>


            <div className="search-container">

              <span>
                🔍
              </span>

              <input
                type="text"
                placeholder="Search contacts..."
                value={search}
                onChange={(event) =>
                  setSearch(event.target.value)
                }
              />

            </div>

          </div>


          {loading ? (

            <div className="empty-state">
              <div className="loading">
                Loading contacts...
              </div>
            </div>

          ) : filteredContacts.length === 0 ? (

            <div className="empty-state">


              <h3>
                No contacts found
              </h3>

              <p>
                Try another search or add a new contact.
              </p>

            </div>

          ) : (

            <div className="table-container">

              <table>

                <thead>

                  <tr>
                    <th>Contact ID</th>
                    <th>Name</th>
                    <th>Phone</th>
                    <th>Email</th>
                    <th>Actions</th>
                  </tr>

                </thead>


                <tbody>

                  {filteredContacts.map(
                    ([id, contact]) => (

                      <tr key={id}>

                        <td>
                          <span className="id-badge">
                            {id}
                          </span>
                        </td>

                        <td>
                          <strong>
                            {contact.name}
                          </strong>
                        </td>

                        <td>
                          {contact.phone}
                        </td>

                        <td>
                          {contact.email}
                        </td>

                        <td>

                          <div className="actions">

                            <button
                              className="edit-btn"
                              onClick={() =>
                                handleEdit(id)
                              }
                            >
                              Edit
                            </button>

                            <button
                              className="delete-btn"
                              onClick={() =>
                                handleDelete(id)
                              }
                            >
                              Delete
                            </button>

                          </div>

                        </td>

                      </tr>

                    )
                  )}

                </tbody>

              </table>

            </div>

          )}

        </section>


        {/* Dictionary explanation */}

        <section className="dictionary-info">

          <div className="dictionary-code">

            <span className="code-label">
              PYTHON DICTIONARY
            </span>

            <pre>{`contacts = {
    "C001": {
        "name": "Name",
        "phone": "1234567890",
        "email": "name@gmail.com"
    }
}`}</pre>

          </div>


          <div className="dictionary-text">

            <h3>
              How this project uses dictionaries
            </h3>

            <p>
              Each Contact ID acts as a dictionary key,
              while the name, phone and email are stored
              as the corresponding value.
            </p>

            <div className="concepts">

              <span>Key-Value Pairs</span>
              <span>CRUD</span>
              <span>Validation</span>
              <span>Python</span>

            </div>

          </div>

        </section>

      </main>


      <footer>
        <strong>Contact Book</strong>
        <span> • </span>
        Python + Flask + React
      </footer>

    </div>
  );
}

export default App;