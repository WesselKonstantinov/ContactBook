# Contact Book command line application
A basic application for saving contact details by using the sqlite3 and click module.

## Setup
1. `git clone https://github.com/WesselKonstantinov/ContactBook.git && cd ContactBook`
2. `pip install -r --user requirements.txt`

## Usage
### Help
For an overview of all commands, run `python3 contacts.py -h` or `python3 contacts.py --help`. This will output:
```
Usage: contacts.py [OPTIONS] COMMAND [ARGS]...

Options:
  -h, --help  Show this message and exit.

Commands:
  add     Create and store new contact details in database.
  delete  Delete contact details of a given person.
  edit    Edit contact details of a given person.
  search  Search contacts by name.
  view    View contact details of either one person or all people.
```
### Commands 
#### add
##### Function
```
$ python3 contacts.py add --help
Usage: contacts.py add [OPTIONS] NAME

  Create and store new contact details in database.

Options:
  -pn, --phone-number TEXT   Phone number of a given person
  -ea, --email-address TEXT  Email address of a given person
  -h, --help                 Show this message and exit.
```
##### Example
To add a new contact, you just need to enter a name and optionally a telephone number and/or email address:
```
python3 contacts.py add 'Floris van Ieperen' --phone-number 0612345678
```
```
python3 contacts.py add 'Hector Kamps' --email-address h.kamps@gmail.com
```
These will respectively output:
```
Added Floris van Ieperen to contact book.
```
```
Added Hector Kamps to contact book.
```

#### view
##### Function
```
$ python3 contacts.py view --help
Usage: contacts.py view [OPTIONS]

  View contact details of either one person or all people.

Options:
  -i, --id INTEGER  Contact id of a given person
  -h, --help        Show this message and exit.
```
##### Example
Running `python3 contacts.py view` will display an overview of all stored contacts:
```
+------------+--------------------+--------------+-------------------+
| contact_id |        name        | phone_number |   email_address   |
+------------+--------------------+--------------+-------------------+
|     1      | Floris van Ieperen |  0612345678  |        None       |
|     2      |    Hector Kamps    |     None     | h.kamps@gmail.com |
+------------+--------------------+--------------+-------------------+
```
It is also possible to display the contact details of one person by suppyling an id:
```
$ python3 contacts.py view --id 2
+------------+--------------+--------------+-------------------+
| contact_id |     name     | phone_number |   email_address   |
+------------+--------------+--------------+-------------------+
|     2      | Hector Kamps |     None     | h.kamps@gmail.com |
+------------+--------------+--------------+-------------------+
```

#### edit
##### Function
```
$ python3 contacts.py edit --help
Usage: contacts.py edit [OPTIONS] ID

  Edit contact details of a given person.

Options:
  -n, --name TEXT            Name of a given person
  -pn, --phone-number TEXT   Phone number of a given person
  -ea, --email-address TEXT  Email address of a given person
  -h, --help                 Show this message and exit.
```
##### Example
To edit the contact details of a person, enter their contact id along with the information you would like to edit:
```
$ python3 contacts.py edit 1 --email-address f.vanieperen@hotmail.com
```
This will output:
```
Successfully updated contact details.
```
Running `python3 contacts.py view --id 1` will show the updated contact details:
```
+------------+--------------------+--------------+--------------------------+
| contact_id |        name        | phone_number |      email_address       |
+------------+--------------------+--------------+--------------------------+
|     1      | Floris van Ieperen |  0612345678  | f.vanieperen@hotmail.com |
+------------+--------------------+--------------+--------------------------+
```

#### delete
##### Function
```
$ python3 contacts.py delete --help
Usage: contacts.py delete [OPTIONS] ID

  Delete contact details of a given person.

Options:
  -h, --help  Show this message and exit.
```
##### Example
To delete the contact details of a person, enter their contact id:
```
$ python3 contacts.py delete 2
```
This will output:
```
Successfully deleted contact.
```
To make sure the contact details of a given person no longer exist, you can run the same command again, which will output:
```
$ python3 contacts.py delete 2
Contact not found.
```
#### search
##### Function
```
$ python3 contacts.py search --help
Usage: contacts.py search [OPTIONS] NAME

  Search contacts by name.

Options:
  -h, --help  Show this message and exit.
```
##### Example
To find the contact details of a person, you just need to enter a name. This will produce a table of all contacts matching the name you have entered:
```
$ python3 contacts.py search floris
+------------+--------------------+--------------+--------------------------+
| contact_id |        name        | phone_number |      email_address       |
+------------+--------------------+--------------+--------------------------+
|     1      | Floris van Ieperen |  0612345678  | f.vanieperen@hotmail.com |
+------------+--------------------+--------------+--------------------------+
```
In case no matching contacts have been found, an empty table will be output to the screen:
```
$ python3 contacts.py search hector
+------------+------+--------------+---------------+
| contact_id | name | phone_number | email_address |
+------------+------+--------------+---------------+
+------------+------+--------------+---------------+
```