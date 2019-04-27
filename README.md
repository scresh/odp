<h1><b>Secure Web Application :: Ochrona Danych Projekt</b></h1>
<p>
  Individual project from the Data Security in Information Technology Systems course at the Warsaw University of Technology.
  App is written in <i>Python 2.7</i>, primarily based on <a href="https://goope.ee.pw.edu.pl/bach/vial">Vial</a> and <a href="http://jinja.pocoo.org/docs/2.10/">Jinja2</a>.
</p>

**UPDATE: It is one of my first Python apps, so please be understanding ;)**

Functionality:
- Strict verification of data from all forms
- Storing password hashes with salt
- Uploading files with any extension
- Sending public code snippets
- Security tokens (against XSRF attacks)
- Hashing password multiple times
- Verifying the number of unsuccessful login attempts
- Password verification delay (against brute-force attacks)
- Checking password difficulty (its entropy)
- Ability to regain access to accout using e-mail 
- Possibility to change password
- Informing users about new connections to their account
