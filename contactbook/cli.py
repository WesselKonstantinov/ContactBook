import click
from prettytable import from_db_cursor
from . import db


# Command-line setup
@click.group()
def cli():
    pass


@click.command()
@click.argument('name')
@click.option('-pn', '--phone-number', help='Phone number of a given person')
@click.option('-ea', '--email-address', help='Email address of a given person')
def add(name, phone_number, email_address):
    """Create and store new contact details in database."""
    contact = {
        'name': name,
        'phone_number': phone_number,
        'email_address': email_address,
    }
    db.cursor.execute("""INSERT INTO contacts (
            name,
            phone_number,
            email_address
        ) VALUES (?, ?, ?)""", (
        contact['name'],
        contact['phone_number'],
        contact['email_address']
    ))
    db.connection.commit()
    db.connection.close()
    click.echo(f'Added {name} to contact book.')


@click.command()
@click.option('-i', '--id', help='Contact id of a given person', type=int)
def view(id):
    """View contact details of either one person or all people."""
    if id:
        db.cursor.execute('SELECT * FROM contacts WHERE contact_id = ?', (id,))
    else:
        db.cursor.execute('SELECT * FROM contacts')

    contacts_table = from_db_cursor(db.cursor)
    click.echo(contacts_table)

    db.connection.close()


@click.command()
@click.argument('id', type=int)
@click.option('-n', '--name', help='Name of a given person')
@click.option('-pn', '--phone-number', help='Phone number of a given person')
@click.option('-ea', '--email-address', help='Email address of a given person')
def edit(id, name, phone_number, email_address):
    """Edit contact details of a given person."""
    db.cursor.execute('SELECT * FROM contacts WHERE contact_id = ?', (id,))
    contact = db.cursor.fetchone()
    if contact:
        if name:
            db.cursor.execute(
                'UPDATE contacts SET name = ? WHERE contact_id = ?',
                (name, id)
            )
        if phone_number:
            db.cursor.execute(
                'UPDATE contacts SET phone_number = ? WHERE contact_id = ?',
                (phone_number, id)
            )
        if email_address:
            db.cursor.execute(
                'UPDATE contacts SET email_address = ? WHERE contact_id = ?',
                (email_address, id)
            )
        db.connection.commit()
        db.connection.close()
        click.echo('Successfully updated contact details.')
    else:
        click.echo('Contact not found.')


@click.command()
@click.argument('id', type=int)
def delete(id):
    """Delete contact details of a given person."""
    db.cursor.execute('SELECT * FROM contacts WHERE contact_id = ?', (id,))
    contact = db.cursor.fetchone()
    if contact:
        db.cursor.execute('DELETE FROM contacts WHERE contact_id = ?', (id,))
        db.connection.commit()
        db.connection.close()
        click.echo('Successfully deleted contact.')
    else:
        click.echo('Contact not found.')


@click.command()
@click.argument('name')
def search(name):
    """Search contacts by name."""
    db.cursor.execute(
        'SELECT * FROM contacts WHERE name LIKE ?',
        (f'%{name}%',)
    )
    contacts_table = from_db_cursor(db.cursor)
    click.echo(contacts_table)

    db.connection.close()


def main():
    """Starting point of the application."""
    commands = [add, view, edit, delete, search]
    for command in commands:
        cli.add_command(command)

    db.setup_contacts_table()
    cli()
