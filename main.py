#import SQLAlchemy as SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta



app = Flask(__name__)
app.secret_key = "hello" #we should put a harder key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=5) #we are gonna store our permanent sessions data for 5 days

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route("/")
def home():
    #also i need to add name on  def home(name):
    #return render_template("index.html", content=["tim", "joe", "bill"], content2=name, r=2)
    return render_template("index.html", content="Testing")

@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())

@app.route("/testingchild")
def testingchild():
    return render_template("testingchild.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True #this define our session as permanent and store the user data as long as especified above
        user = request.form["nm"]
        session["user"] = user
        found_user = users.query.filter_by(name = user).first()
        if found_user:
            session["email"] = found_user.email

        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit() #every change in the database need to be commited


        flash("Login Succesful!")
        return redirect(url_for("user"))
    else:
        if "user" in session: #if we are already loged in
            flash("Already Logged In!")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user", methods =["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved!")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    #if "user" in session:#if there are any user in the session and they logged out we will show a message
        #user = session["user"]
    flash(f"you have been logged out", "info")
    session.pop("user", None) # we remove user data from my sessions
    session.pop("email", None)
    return redirect(url_for("login"))


'''
app.permanent_session_lifetime = timedelta(minutes=5) #we are gonna store our permanent sessions data for 5 days


@app.route("/")
def home():
    #also i need to add name on  def home(name):
    #return render_template("index.html", content=["tim", "joe", "bill"], content2=name, r=2)
    return render_template("index.html", content="Testing")

@app.route("/testingchild")
def testingchild():
    return render_template("testingchild.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True #this define our session as permanent and store the user data as long as especified above
        user = request.form["nm"]
        session["user"] = user
        flash("Login Succesful!")
        return redirect(url_for("user"))
    else:
        if "user" in session: #if we are already loged in
            flash("Already Logged In!")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user.html", user=user)
    else:
        flash("You are not logged in!")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    #if "user" in session:#if there are any user in the session and they logged out we will show a message
        #user = session["user"]
    flash(f"you have been logged out", "info")
    session.pop("user", None) # we remove user data from my sessions
    return redirect(url_for("login"))
'''

'''
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return redirect(url_for("user", usr=user))
    else:
        return render_template("login.html")


@app.route("/<usr>")
def user(usr):
    return f"<h1>{usr}</h1>"
'''

# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}"
#
# @app.route("/admin/")
# def admin():
#     return redirect(url_for("user", name="Admin!"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

