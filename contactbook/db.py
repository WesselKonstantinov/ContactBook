import sqlite3


# Database setup
connection = sqlite3.connect('contact_book.db')
cursor = connection.cursor()


def setup_contacts_table():
    """Set up table for storing contact info."""
    cursor.execute("""CREATE TABLE IF NOT EXISTS contacts (
        contact_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        phone_number TEXT UNIQUE,
        email_address TEXT UNIQUE)""")
