import sqlite3
import click
from prettytable import from_db_cursor

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


@click.command()
@click.option('-i', '--id', help='Contact id of a given person', type=int)
def view(id):
    """View contact details of either one person or all people."""
    if id:
        cursor.execute('SELECT * FROM contacts WHERE contact_id = ?', (id,))
    else:
        cursor.execute('SELECT * FROM contacts')

    contacts_table = from_db_cursor(cursor)
    click.echo(contacts_table)

    connection.close()


@click.command()
@click.argument('id', type=int)
@click.option('-n', '--name', help='Name of a given person')
@click.option('-pn', '--phone-number', help='Phone number of a given person')
@click.option('-ea', '--email-address', help='Email address of a given person')
def edit(id, name, phone_number, email_address):
    """Edit contact details of a given person."""
    cursor.execute('SELECT * FROM contacts WHERE contact_id = ?', (id,))
    contact = cursor.fetchone()
    if contact:
        if name:
            cursor.execute(
                'UPDATE contacts SET name = ? WHERE contact_id = ?',
                (name, id)
            )
        if phone_number:
            cursor.execute(
                'UPDATE contacts SET phone_number = ? WHERE contact_id = ?',
                (phone_number, id)
            )
        if email_address:
            cursor.execute(
                'UPDATE contacts SET email_address = ? WHERE contact_id = ?',
                (email_address, id)
            )
        connection.commit()
        connection.close()
        click.echo('Successfully updated contact details.')
    else:
        click.echo('Contact not found.')


@click.command()
@click.argument('id', type=int)
def delete(id):
    """Delete contact details of a given person."""
    cursor.execute('SELECT * FROM contacts WHERE contact_id = ?', (id,))
    contact = cursor.fetchone()
    if contact:
        cursor.execute('DELETE FROM contacts WHERE contact_id = ?', (id,))
        connection.commit()
        connection.close()
        click.echo('Successfully deleted contact.')
    else:
        click.echo('Contact not found.')


cli.add_command(add)
cli.add_command(view)
cli.add_command(edit)
cli.add_command(delete)

if __name__ == '__main__':
    setup_contacts_table()
    cli()
