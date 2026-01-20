import os
import re
import uuid
from flask import Flask, request, render_template, send_file
from werkzeug.utils import secure_filename

from topsis_harith_102303243.topsis import validate_and_load, run_topsis, TopsisError

# -----------------------------------
# Config
# -----------------------------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

EMAIL_REGEX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# -----------------------------------
# Optional Email Functionality
# -----------------------------------
def send_email(to_email, file_path):
    """
    Optional: Only works if credentials are set and correct.
    """
    import smtplib
    from email.message import EmailMessage

    sender_email = os.getenv("SENDER_EMAIL")
    sender_pass = os.getenv("SENDER_PASSWORD")

    if not sender_email or not sender_pass:
        raise Exception("Email credentials not set in env variables.")

    msg = EmailMessage()
    msg["Subject"] = "TOPSIS Result File"
    msg["From"] = sender_email
    msg["To"] = to_email
    msg.set_content("Hello,\n\nAttached is your TOPSIS result file.\n\nThanks")

    with open(file_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="text",
            subtype="csv",
            filename=os.path.basename(file_path),
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, sender_pass)
        smtp.send_message(msg)


# -----------------------------------
# Routes
# -----------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    try:
        # inputs
        file = request.files.get("file")
        weights = request.form.get("weights", "").strip()
        impacts = request.form.get("impacts", "").strip()
        email = request.form.get("email", "").strip()

        if not file or file.filename == "":
            return render_template("index.html", error="Please upload a CSV file.")

        if weights == "" or impacts == "":
            return render_template("index.html", error="Weights and impacts cannot be empty.")

        if email != "" and not re.match(EMAIL_REGEX, email):
            return render_template("index.html", error="Invalid email format.")

        # Save uploaded file
        filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())[:8]
        input_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{unique_id}_{filename}")
        file.save(input_path)

        # Output path
        output_filename = f"topsis_result_{unique_id}.csv"
        output_path = os.path.join(app.config["UPLOAD_FOLDER"], output_filename)

        # TOPSIS
        df, criteria_cols, w, im = validate_and_load(input_path, weights, impacts)
        out = run_topsis(df, criteria_cols, w, im)
        out.to_csv(output_path, index=False)

        # Preview (top 8 rows)
        preview_html = out.head(8).to_html(classes="table table-striped table-hover", index=False)

        # Try sending mail (optional)
        email_status = None
        if email:
            try:
                send_email(email, output_path)
                email_status = f"✅ Result emailed successfully to {email}"
            except Exception as e:
                email_status = f"⚠️ Email could not be sent: {str(e)}"

        return render_template(
            "index.html",
            success="TOPSIS evaluation completed successfully!",
            uploaded_file=filename,
            output_file=output_filename,
            preview_table=preview_html,
            email_status=email_status
        )

    except TopsisError as e:
        return render_template("index.html", error=f"TOPSIS Error: {str(e)}")
    except Exception as e:
        return render_template("index.html", error=f"Server Error: {str(e)}")


@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if not os.path.exists(file_path):
        return "File not found", 404

    return send_file(file_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
