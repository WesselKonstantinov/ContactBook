import sqlite3
import click


# Database setup
connection = sqlite3.connect('contact_book.db')
cursor = connection.cursor()


def setup_contacts_table():
    """Set up table for storing contact info."""
    cursor.execute("""CREATE TABLE IF NOT EXISTS contacts (
        contact_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        phone_number TEXT NOT NULL UNIQUE,
        email_address TEXT NOT NULL UNIQUE)""")


# Command-line setup
@click.group()
def cli():
    pass


@click.command()
@click.argument('name')
@click.argument('phone_number')
@click.argument('email_address')
def add(name, phone_number, email_address):
    """Create and store new contact details in database."""
    cursor.execute("""INSERT INTO contacts (
            name,
            phone_number,
            email_address
        ) VALUES (?, ?, ?)""", (name, phone_number, email_address))
    connection.commit()
    connection.close()
    click.echo(f'Saved contact details of {name}.')


cli.add_command(add)

if __name__ == '__main__':
    setup_contacts_table()
    cli()
