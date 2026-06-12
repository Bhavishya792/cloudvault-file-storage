import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user,
)

from dotenv import load_dotenv

from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from werkzeug.utils import secure_filename

from models import db, User, File, Activity

from s3_utils import upload_file_to_s3, generate_download_url, delete_file_from_s3

load_dotenv()


app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cloudvault.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db.init_app(app)


login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):

    return User.query.get(int(user_id))


@app.route("/")
def home():

    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_username = User.query.filter_by(username=username).first()

        if existing_username:

            flash("Username already exists")

            return redirect(url_for("register"))

        existing_email = User.query.filter_by(email=email).first()

        if existing_email:

            flash("Email already exists")

            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
        )

        db.session.add(new_user)

        db.session.commit()

        flash("Account created successfully")

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        identifier = request.form.get("identifier")
        password = request.form.get("password")

        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier)
        ).first()

        if not user:

            flash("User not found")

            return redirect(url_for("login"))

        if not check_password_hash(user.password_hash, password):

            flash("Incorrect password")

            return redirect(url_for("login"))

        login_user(user)

        flash("Logged in successfully")

        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard")
@login_required
def dashboard():

    search = request.args.get("search", "")

    query = File.query.filter_by(user_id=current_user.id)

    if search:

        query = query.filter(File.filename.contains(search))

    files = query.order_by(File.uploaded_at.desc()).all()

    activities = (
        Activity.query.filter_by(user_id=current_user.id)
        .order_by(Activity.created_at.desc())
        .limit(8)
        .all()
    )

    total_files = len(files)

    total_versions = len(files)

    latest_file = (
        files[0].filename[:20] + "..."
        if files and len(files[0].filename) > 20
        else (files[0].filename if files else "None")
    )

    storage_used = round(sum(file.file_size or 0 for file in files) / (1024 * 1024), 2)

    return render_template(
        "dashboard.html",
        user=current_user,
        files=files,
        activities=activities,
        total_files=total_files,
        total_versions=total_versions,
        storage_used=storage_used,
        latest_file=latest_file,
        search=search,
    )


@app.route("/upload", methods=["POST"])
@login_required
def upload():

    file = request.files.get("file")

    if not file:

        flash("No file selected")

        return redirect(url_for("dashboard"))

    filename = secure_filename(file.filename)

    existing_versions = File.query.filter_by(
        filename=filename, user_id=current_user.id
    ).count()

    version = existing_versions + 1

    s3_key = f"user_{current_user.id}/" f"{filename}_v{version}"

    file.seek(0, os.SEEK_END)

    size = file.tell()

    file.seek(0)

    upload_file_to_s3(file, s3_key)

    file_record = File(
        filename=filename,
        s3_key=s3_key,
        version=version,
        user_id=current_user.id,
        file_size=size,
    )

    db.session.add(file_record)

    activity = Activity(action=f"Uploaded {filename}", user_id=current_user.id)

    db.session.add(activity)

    db.session.commit()

    flash("File uploaded successfully")

    return redirect(url_for("dashboard"))


@app.route("/download/<int:file_id>")
@login_required
def download_file(file_id):

    file = File.query.get_or_404(file_id)

    if file.user_id != current_user.id:

        flash("Access denied")

        return redirect(url_for("dashboard"))

    url = generate_download_url(file.s3_key)

    return redirect(url)


@app.route("/share/<int:file_id>")
@login_required
def share_file(file_id):

    file = File.query.get_or_404(file_id)

    if file.user_id != current_user.id:

        flash("Access denied")

        return redirect(url_for("dashboard"))

    share_url = generate_download_url(file.s3_key)
    activity = Activity(action=f"Shared {file.filename}", user_id=current_user.id)

    db.session.add(activity)

    db.session.commit()

    return render_template("share.html", share_url=share_url)


@app.route("/delete/<int:file_id>")
@login_required
def delete_file(file_id):

    file = File.query.get_or_404(file_id)

    if file.user_id != current_user.id:

        flash("Access denied")

        return redirect(url_for("dashboard"))

    delete_file_from_s3(file.s3_key)

    db.session.delete(file)

    activity = Activity(action=f"Deleted {file.filename}", user_id=current_user.id)

    db.session.add(activity)

    db.session.commit()

    flash("File deleted successfully")

    return redirect(url_for("dashboard"))


@app.route("/versions/<string:filename>")
@login_required
def versions(filename):

    versions = (
        File.query.filter_by(filename=filename, user_id=current_user.id)
        .order_by(File.version.desc())
        .all()
    )

    return render_template("versions.html", filename=filename, versions=versions)


@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out")

    return redirect(url_for("login"))


if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
