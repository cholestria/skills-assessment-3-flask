from flask import Flask, request, render_template, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
import jinja2


app = Flask(__name__)


# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


@app.route("/")
def index():
    """Return homepage."""

    return render_template("index.html")


@app.route("/application-form")
def application_form():
    """Return application form."""

    jobs_list = ['Software Engineer', 'QA Engineer', 'Product Management']

    return render_template("application-form.html",
                            jobs_list=jobs_list)


@app.route("/application-form", methods=["POST"])
def application_response():
    """Return success message."""

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    job = request.form["job"]
    salary = request.form["salary"]

    if validate_form(request.form):
        return render_template("application-response.html",
                                first_name=first_name,
                                last_name=last_name,
                                job=job,
                                salary=salary)
    else:
        return redirect('application-form')


def validate_form(form):
    """Determine form input validity"""

    is_valid = True
    salary = form["salary"]

    try:
        salary = float(salary)
        if salary <= 0:
            flash("Please enter a salary above 0.")
            is_valid = False
    except ValueError:
        is_valid = False
        flash("Please enter a number for salary.")

    if len(form["first-name"]) <= 0 or len(form["last-name"]) <= 0:
        is_valid = False
        flash("Please enter your name")

    return is_valid


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
