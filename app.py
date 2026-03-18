from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/parent")
def parent_dashboard():
    return render_template("parent_dashboard.html")

@app.route("/child")
def child_dashboard():
    return render_template("child_dashboard.html")


@app.route("/communication")
def communication():
    return render_template("communication.html")

@app.route("/social")
def social():
    return render_template("social.html")

@app.route("/cognitive")
def cognitive():
    return render_template("cognitive.html")

@app.route("/daily")
def daily():
    return render_template("daily.html")
@app.route("/color-match")
def color_match():
    return render_template("color_match.html")

@app.route("/object-identification")
def object_identification():
    return render_template("object_identification.html")

@app.route("/activity-completed")
def activity_completed():
    return render_template("activity_completed.html")

@app.route("/parent/progress")
def parent_progress():
    return render_template("parent_progress.html")

@app.route("/admin")
def admin_dashboard():
    return render_template("admin/admin_dashboard.html")

@app.route("/admin/modules")
def manage_modules():
    return render_template("admin/manage_modules.html")

@app.route("/admin/reports")
def view_reports():
    return render_template("admin/view_reports.html")




if __name__ == "__main__":
    app.run(debug=True)
