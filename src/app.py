from cmath import isfinite
from crypt import methods
import json
import os
import ssl
import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import Flask, request, render_template
from flask_cors import CORS
from barcode import Code128
from barcode.writer import ImageWriter

from src.db.users import create_user, delete_all_users, get_users, get_user_data, delete_user, get_last_user_ID, update_user, check_arrival, change_status, check_validity, delete_all_users, user_data


app = Flask(__name__)
cors = CORS(app)


### routes ###

#index
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


#dohvati sve
@app.route("/users", methods=["GET"])
def return_users():
    return get_users()


@app.route("/user_list", methods=["GET"])
def user_list():
    return render_template("user_list.html")


#stvori novog
@app.route("/register", methods=["POST"])
def create():
    request_data = request.get_json()
    start_bracket = "{"
    end_bracket = "}"

    start_bracket += request_data
    start_bracket += end_bracket

    request_data = start_bracket

    json_object = json.loads(request_data)

    first_name = json_object["first_name"]
    last_name = json_object["last_name"]
    title = json_object["title"]
    email = json_object["email"]


    create_user(first_name=first_name, last_name=last_name, title=title, email=email)
    print("uspješno kreiran korisnik")

    emailHandler(first_name, last_name, title, email, get_last_user_ID())

    return render_template("add_user.html")


@app.route("/new_user", methods=["GET"])
def new_user():
    return render_template("add_user.html")


#provjera dolaska
@app.route("/check_arrival/<user_id>", methods=["GET"])
def security_check(user_id):
    return check_arrival(user_id)

@app.route("/check_validity/<user_id>", methods=["GET"])
def validity_check(user_id):
    return check_validity(user_id)

@app.route("/change_status/<user_id>", methods=["GET"])
def change(user_id):
    return change_status(user_id)


#dohvati podatke jednog
@app.route("/users/<user_id>", methods=["GET"])
def fetch_data(user_id):
    return get_user_data(user_id)

@app.route("/data/<user_id>", methods = ["GET"])
def get_data(user_id):
    return user_data(user_id)


#izbrisi jednog
@app.route("/remove", methods=["POST"])
def remove_user():
    json_object = json.loads(adjustData(request.get_json()))

    user_id = json_object["id"]
    delete_user(user_id=user_id)
    return render_template("user_list.html")


#izbrisi sve
@app.route("/delete_all_users", methods = ["GET"])
def delete_all():
    delete_all_users()
    return render_template("user_list.html")

#azuriraj jednog
@app.route("/update", methods=["POST"])
def update():
    json_object = json.loads(adjustData(request.get_json()))

    first_name = json_object["first_name"]
    last_name = json_object["last_name"]
    title = json_object["title"]
    email = json_object["email"]
    id = json_object["id"]

    update_user(first_name=first_name, last_name=last_name, title=title, email=email, user_id=id)
    return render_template("user_list.html")


#skreniraj qr
@app.route("/scanqr", methods=["GET","POST"])
def scan_qr():
    return render_template("scanqr.html")


@app.route("/send_email", methods = ["POST"])
def send_Email():
    json_object = json.loads(adjustData(request.get_json()))

    first_name = json_object["first_name"]
    last_name = json_object["last_name"]
    title = json_object["title"]
    email = json_object["email"]
    id = json_object["id"]

    print(first_name, last_name, title, email, id)

    emailHandler(first_name = first_name, last_name = last_name, title = title, email = email, id = id)
    return render_template("user_list.html")


### helpers ###

def emailHandler(first_name, last_name, title, email, id):
    if (type(id) == str):
        number = id
    else: 
        number = id[0]
        number = str(number)

    

    barcode = Code128(number, writer=ImageWriter())
    barcode.save("barcode")

    email_sender = 'neoscan.test@gmail.com'
    email_password = os.environ.get("MAIL_PASSWORD")
    email_receiver = email
    subject = 'Hvala na registraciji!'
  
    em = MIMEMultipart("alternative")
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject

    filename = "barcode.png"

    html = emailBody(first_name, last_name, title)

    part = MIMEText(html, "html")
    em.attach(part)

    with open (filename, "rb") as attachment: 
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    
    encoders.encode_base64(part)

    part.add_header(
        "Content-Disposition",
        "attachment", filename = filename
    )
    em.attach(part)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def adjustData (request_data):
    start_bracket = "{"
    end_bracket = "}"

    start_bracket += request_data
    start_bracket += end_bracket

    request_data = start_bracket

    return request_data

def emailBody(first_name, last_name, title):
    html ="""\
    <html>
        <body>
            <div>
                Pozdrav <b>{first_name} {last_name}</b>!<br><br>

                Ovaj email je potvrda Vaše registracije na konferenciju.<br>
                Vaša karta ima kategoriju <b>{title}</b>.<br>
                <br>
                U prilogu možete pronaći vlastiti barkod na osnovu kojeg ćete na ulasku dobiti vlastitu akreditaciju. <br>
                Ako želite, možete ga isprintati, ali nije obavezno. Dovoljno je da ga pokažete na svom mobilnom uređaju pri dolasku.<br>
                <br>
                Hvala Vam za sudjelovanje na konferenciji i vidimo se uskoro! <br>
            </div>
        </body>
    </html>
    """.format(first_name = first_name, last_name = last_name, title = title)

    return html

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)