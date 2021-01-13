from flask import *
from flask_mail import Mail, Message
import json
import time
import os

from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.utils import secure_filename
#borafuncionar?
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'

allowed_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
c =[]
b = []
users = []
servidor = ''
porta = ''

@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')

def set_porta_serv(i):
    if 'gmail.com' in i.get('select'):
        servidor = 'smtp.gmail.com'
        porta = 587
        return [servidor, porta]
    elif 'outlook' in i.get('select'):
        servidor = 'smtp-mail.outlook.com'
        porta = 587
        return [servidor, porta]

    elif 'uol.com.br' in i.get('select'):
        servidor = 'smtps.uol.com.br'
        porta = 587
        return [servidor, porta]

    elif 'aol.com' in i.get('select'):
        servidor = 'smtp.aol.com'
        porta = 587
        return [servidor, porta]

    elif 'office365' in i.get('select'):
        servidor = 'smtp.office365.com'
        porta = 587
        return [servidor, porta]

    elif 'smtp.live.com' in i.get('select'):
        servidor = 'smtp.live.com'
        porta = 465
        return [servidor, porta]

    elif 'smtp.mail.yahoo.com' in i.get('select'):
        servidor = 'smtp.mail.yahoo.com'
        porta = 465
        return [servidor, porta]


def send_mail(i,dado_mail):
    [servidor, porta] = set_porta_serv(i)
    
    app.config['MAIL_SERVER'] = servidor
    app.config['MAIL_PORT'] = porta
    app.config['MAIL_USERNAME'] = i.get('email')
    app.config['MAIL_PASSWORD'] = i.get('senha')
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_SUPPRESS_SEND'] = False
    app.config['MAIL_MAX_EMAILS'] = 25
    app.config['MAIL_DEFAULT_SENDER'] = ""
    mail = Mail(app)
    with mail.connect() as conn:
        for user in users:
            msg = Message(subject=dado_mail[1].get('subject'), sender=i.get('email'), recipients=[user])
            msg.html = dado_mail[0].get('mailBody')
            conn.send(msg)
            print('email sent to: ' + user + '  from: ' + i.get('email'))
            b.append(user)
            if len(users) > 25:
                if user > users[25]:
                    print('break')
                    break

def send_mail_teste(i,dado_mail):
    email_subject = dado_mail[1].get('subject')
    email_sender = i.get('email')
    recipiente = dado_mail[2].get('emailTest')
    corpo_mensagem = dado_mail[0].get('mailBody')

    [servidor, porta] = set_porta_serv(i)
    app.config['MAIL_SERVER'] = servidor
    app.config['MAIL_PORT'] = porta
    app.config['MAIL_USERNAME'] = i.get('email')
    app.config['MAIL_PASSWORD'] = i.get('senha')
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_SUPPRESS_SEND'] = False
    app.config['MAIL_MAX_EMAILS'] = 20
    app.config['MAIL_DEFAULT_SENDER'] = ""
    mail = Mail(app)
    msg = Message(subject=email_subject,  recipients=[recipiente], sender=email_sender)
    msg.html = corpo_mensagem
    mail.send(msg)
    # print('email sent  '+ recipiente + '  from: ' + email_sender)
                
def addMails(file):
    f = open(os.path.join(app.config['UPLOAD_FOLDER'],file), 'r')
    f1 = f.read().rsplit(",")
    # f1 = f.read().splitlines()
    for x in f1:
        users.append(x)
    users.pop()
    users.sort()

def limpar():
    for ii in b:
        if ii in users:
            users.remove(ii)




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route("/api/read_contents", methods=['POST'])
def index_read():
    # if request.method == 'POST' and 'file_text' in request.files:
    isthisFileText=request.files.get('email_body_text_file')
    isthisFileMails=request.files.get('mails_text_file')

    print(isthisFileText)
    print(isthisFileMails)
    filename = secure_filename(isthisFileMails.filename)
    isthisFileMails.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    addMails(filename)
    #     flash("Photo saved.")


    return jsonify({"code": 200, "status": "Listas enviadas"})


@app.route("/api/send_mail", methods=['POST'])
def index_route():
    data = dict(request.form)
    new_data = json.loads(data['data'])
    dado_mail = []
    total = ''
    dado_mail.append(new_data[4])
    dado_mail.append(new_data[5])
    new_data.pop(4)
    new_data.pop(4)
    while len(users) > 0:
        for i in new_data:
            if 'vazio166' == i.get('email'):
                break
            else:
                limpar()
                send_mail(i,dado_mail)
        time.sleep(60)        
    limpar()
    total = len(b)
    clearB()
    
        
    
    return {
        "status": "okay",
        "code": 200,
        "total": total
    }


@app.route("/api/send_mail_teste", methods=['POST'])
def index_teste():
    data = dict(request.form)
    new_data = json.loads(data['data'])
    dado_mail = []
    total = ''
    c = []
    dado_mail.append(new_data[4])
    dado_mail.append(new_data[5])
    dado_mail.append(new_data[6])
    new_data.pop(4)
    new_data.pop(4)
    new_data.pop(4)
    for i in new_data:
        if 'vazio166' == i.get('email'):
                break
        else:
            send_mail_teste(i,dado_mail)
            c.append('um')
    total = len(c)
    c = []
        
    
    return {
        "status": "okay",
        "code": 200,
        "total": total
    }



def clearB():
    b.clear()
    print('b cleared')


if __name__ == "__main__":

    app.run(debug=True)
