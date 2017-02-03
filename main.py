import webapp2
import re
import cgi

#create a function to validate a username
user_re = re.compile(r"^[a-zA-Z0-9_-]{6,20}$")
def valid_username(username):
    return user_re.match(username)

#create a function to validate a password
password_re = re.compile(r"^[a-zA-Z0-9]{6,20}$")
def valid_password(password):
        return password_re.match(password)

def verify_password(password, password2):
    if password == password2:
        return password_re.match(password2)

#create a function to validate an e-mail
email_re = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return email_re.match(email)

#create an escape_html function
def escape_html(s):
    return cgi.escape(s, quote = True)

form="""
    <h1>User Signup!</h1>
    <br>
    <form method="post" aciton="/welcome">
        <label>Username:
            <input type="text" name="username" value="%(username)s">
        </label>
        <br>
        <label>Password:
            <input type="password" name="password" value="%(password)s">
        </label>
        <br>
        <label>Verify Password:
            <input type="password" name="second_password" value="%(second_password)s">
        </label>
        <br>
        <label>E-mail(Optional):
            <input type="text" name="email" value="%(email)s">
            <div style="color: red">%(error)s</div>
        </label>
        <br>
        <input type="submit">
    </form>
"""
#put in an checkbox to ask user if they want to be part of our e-mail list

class MainHandler(webapp2.RequestHandler):
    def write_form(self, error="", username="", password="", second_password="", email=""):
        self.response.out.write(form % {"error": error,
                                        "username": escape_html(username),
                                        "password": escape_html(password),
                                        "second_password": escape_html(second_password),
                                        "email": escape_html(email)})

    def get(self):
        self.write_form()

    def post(self):

        input_username = self.request.get('username')
        input_password = self.request.get('password')
        input_second_password = self.request.get('second_password')
        input_email = self.request.get('email')


        username = valid_username(input_username)
        password = valid_password(input_password)
        second_password = verify_password(input_password, input_second_password)
        email = valid_email(input_email)

        if not username:
            self.write_form("Invalid Username", input_username)
        elif not password:
            self.write_form("Invalid Password", input_username)
        elif not second_password:
            self.write_form("Please Verify Password", input_username)
        elif len(input_email) > 0:
            if not email:
                self.write_form("Invalid E-mail", input_username)
            else:
                self.redirect("/welcome?username=" + input_username + "&email=" + input_email)
        else:
            self.redirect("/welcome?username=" + input_username)

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = escape_html(self.request.get("username"))
        email = escape_html(self.request.get("email"))
        contents="<h1>Welcome, " + username + "!</h1>"
        self.response.out.write(contents)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
