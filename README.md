# food_for_you
A python, kivy and sqlite frontend for the Edamam api

### Installation:
- Download the repo, and keep everything saved in the same folder
- Install Python
- Install Kivy via pip
```
$ pip install kivy
```
- On line 418 and 419 in main.py, add your Edamam app id and key

### Running and Use:
Two test accounts have been set up in the db.

Username: test_user1 <br />
Password: Password1

Username: test_user2 <br />
Password: Password2

The ability to add accounts or remove recipes has not been implemented yet. To do so manually, edit the db file and remove recipe entries 
or to add an account, input a sha256 password in the account entry.

