from flask import render_template, request
from . import web_bp


@web_bp.route("/")
def index():
    return render_template("index.html")


@web_bp.route("/form")
def form():
    return render_template("form.html")


@web_bp.route("/results")
def results():
    # The frontend JS will call the API and populate this page
    return render_template("results.html")


@web_bp.route("/feedback")
def feedback():
    return render_template("feedback.html")


