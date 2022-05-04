from email.policy import default
from xmlrpc.client import Boolean
from flask_sqlalchemy import SQLAlchemy

#Modulo per generare hash della password
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from sqlalchemy import MetaData, false

"""
Flask login offre:
- Memorizza l'ID utente nella sessione e i meccanismi per il login e il logout .
- Limita l'accesso a determinate viste solo agli utenti autenticati.
- Gestisci la funzionalità Ricordami  per mantenere la sessione anche dopo che l'utente ha chiuso il browser.
- Proteggi l'accesso ai cookie di sessione di terze parti."""
from flask_login import LoginManager
from flask_security import UserMixin, RoleMixin, login_required

#Problema importazione dell'app dal file app risolto con 
from flask import current_app
#Flask werkzeug ha funzioni integrate per affrontare questo problema.#Problema : non possiamo salvare le password degli utenti
"""
Flask-login utilizza l'autenticazione basata su cookie.
uando il cliente effettua il login tramite le sue credenziali, 
Flask crea una sessione contenente l' ID utente e quindi invia l' ID sessione all'utente tramite un cookie,
 utilizzando il quale può effettuare il login e il logout come e quando richiesto.
"""
#Creazione di un oggetto della classe LoginManager che chiameremo login_manager e collegarlo all'app
login_manager = LoginManager() #creare e inizializzare l'estensione Flask_login.
login_manager.login_view = 'login'

#Creazione dell'oggetto db e collegamento all' pp
db = SQLAlchemy()


#new lines

#tabella user task di supporto per la relazione molti a molti, deve essere dichiarata di tipo Table e deve fare riferimento ai metadata del db , se no non TROVA LE TABELLE
user_tasks=db.Table('user_tasks',db.metadata,
db.Column("user_id",db.Integer, db.ForeignKey('users.id'), primary_key=True),
db.Column("project_id",db.Integer, db.ForeignKey('projects.id'), primary_key=True),

)


#CLASSE TODO
class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    date = db.Column(db.Date())
    time = db.Column(db.Time())
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    category= db.Column(db.String, db.ForeignKey('category.id'))

    checked = db.Column(db.Boolean, default= False)

    def __str__ (self):
        return 'Titolo =' + self.title + 'data =' + str(self.date) + 'time =' + str(self.time) + 'project_id =' +  str(self.project_id) + 'categoria =' + str(self.category)
    def __repr__(self):
        return '<TAsk {}>'.format(self.title)


#CLASSE Projects
class Project(db.Model):
    __tablename__ = 'projects'
 

    id = db.Column(db.String(), primary_key=True)
    
    title = db.Column(db.String(140))
    description = db.Column(db.String())
    image = db.Column(db.String())
    mimetype = db.Column(db.String())
    created_by= db.Column(db.Integer(), primary_key=True)
    #Field (N) in 1 a N

    tasks = db.relationship('Task', backref='author', lazy='dynamic')


    def __str__ (self):
        return 'Titolo =' + self.title + 'description =' + self.description + 'image =' + self.image + 'user ='
    def __repr__(self):
        return '<Project {}>'.format(self.title)


#CLASSE Association
class Association(db.Model):
    __tablename__ = 'user_request'
    user_id_mittente= db.Column("user_id_mittente",db.Integer, db.ForeignKey('users.id'), primary_key=True)
    project_id= db.Column("project_id",db.String, db.ForeignKey('projects.id'), primary_key=True)
    user_id_destinatario= db.Column("user_id_destinatario",db.Integer)
    accepted= db.Column("accepted",db.Boolean, default= False)
    refused= db.Column("refuse", db.Boolean, default= False)
    project = db.relationship("Project")

#CLASSE UTENTE
#L'unico requisito dichiarato da Flask-login è che la classe utente deve implementare le seguenti proprietà e metodi:
# - is_authenticated: una proprietà che indica Truese l'utente è stato autenticato e Falsealtro
# - is_active: una proprietà che indica se l'account dell'utente è attivo ( True) o meno ( False). È tua decisione definire cosa significa che un account utente è attivo. Ad esempio, l'e-mail è stata verificata o non è stata eliminata da un amministratore. Per impostazione predefinita, gli utenti con account inattivi non possono eseguire l'autenticazione.
# - is_anonymous: una proprietà valida False per utenti reali e True per utenti anonimi.
# - get_id(): un metodo che restituisce a string( unicodenel caso di Python 2) con l' IDunivoca dell'utente. Se IDl'utente era into qualsiasi altro tipo, è tua responsabilità convertirlo in string.
#Flask-login ci rende disponibile la classe UserMixincon un'implementazione predefinita per tutte queste proprietà e metodi. 
# Dobbiamo solo ereditare da esso nella nostra stessa classe User.
class UserModel(UserMixin, db.Model):
    #specificare nome tabella
    __tablename__ = 'users'
    
    id = db.Column( db.Integer, primary_key=True)
    email = db.Column(db.String(80))
    username = db.Column(db.String(100))
    password = db.Column(db.String())  
    active= db.Column(db.Boolean(), default= True)  
    is_admin= db.Column(db.Boolean(), default= False)  
    #Field (1) in 1 a N
    projects = db.relationship("Project", secondary=user_tasks,backref='author', lazy ='dynamic')
    requests = db.relationship("Association")
    def remove(self):
        db.session.delete(self)



#CLASSE CATEGORY
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __repr__(self):
        return '<Category {}>'.format(self.name)


class Request():
     def __init__(self,id,id_progetto, titolo_progetto,id_mittente,username_mittente, email_mittente,accepted,refused):
         self.id= id
         self.id_progetto= id_progetto
         self.titolo_progetto= titolo_progetto
         self.id_mittente= id_mittente
         self.username_mittente= username_mittente
         self.email_mittente= email_mittente
         self.accepted= accepted
         self.refused= refused

class Request_done():
      def __init__(self, project, done):
          self.project= project
          self.done= done