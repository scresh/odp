<h1><b>Secure Web Application :: Ochrona Danych Projekt</b></h1>
<p>
  Individual project from the Data Security in Information Technology Systems course at the Warsaw University of Technology.
  App is written in <i>Python 2.7</i>, primarily based on <a href="https://goope.ee.pw.edu.pl/bach/vial">Vial</a> and <a href="http://jinja.pocoo.org/docs/2.10/">Jinja2</a>.
</p>

**UPDATE: It is one of my first Python apps, so please be understanding ;)**

## Functionality:
* Strict verification of data from all forms
* Storing password hashes with salt
* Uploading files with any extension
* Sending public code snippets
* Security tokens (against XSRF attacks)
* Hashing password multiple times
* Verifying the number of unsuccessful login attempts
* Password verification delay (against brute-force attacks)
* Checking password difficulty (its entropy)
* Ability to regain access to accout using e-mail 
* Possibility to change password
* Informing users about new connections to their account


## Usage

Install python packages from <i>requirements.txt</i> :
```bash
pip install -r requirements.txt --user
```

Change server socket in <i>drink.ini</i> file if needed:
```ini
[uwsgi]
socket = 127.0.0.1:1337
protocol = http
module = drink:app
plugins = python
```

Set login credentials for password-reminder e-mail account and (optionally) your domain in <i>params.py</i>:
```python
param_dict = {
    'domain': '127.0.0.1',
    'db_file': 'database.db',
    'mail_user': 'mail.bot@gmail.com',
    'mail_password': 'ExamplePassword1234',
    'mail_smtp': 'smtp.gmail.com',
    'mail_port': 587,
}
```

Run UWSGI with provided config file :
```bash
uwsgi --ini drink.ini
```

## Screenshots
