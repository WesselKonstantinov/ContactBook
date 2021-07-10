import click
from prettytable import from_db_cursor
from . import db


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
    db.cursor.execute("""INSERT INTO contacts (
            name,
            phone_number,
            email_address
        ) VALUES (?, ?, ?)""", (name, phone_number, email_address))
    db.connection.commit()
    db.connection.close()
    click.echo(f'Saved contact details of {name}.')


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


cli.add_command(add)
cli.add_command(view)
cli.add_command(edit)
cli.add_command(delete)
cli.add_command(search)


def main():
    db.setup_contacts_table()
    cli()
