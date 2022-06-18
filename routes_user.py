#Importazione moduli necessari
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user, login_user, logout_user
from form import TaskForm, RegistrationForm, LoginForm
from werkzeug.urls import url_parse
from models import *
from app import app
from flask_wtf import FlaskForm

#PERCORSO DI DEFAULT
@app.route('/')
def index():
  return redirect(url_for('login'))

"""

@app.before_first_request 
def create_user(): 
  db.session.add(UserModel(username= 'admin2' , email='admin2@libero.it', password='admin', is_admin= True))
  db.session.commit()



"""





"""Route dell'autenticazione  e profilo"""

#PERCORSO DI REGISTRAZIONE
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Per prima cosa controlliamo se l'utente corrente è già autenticato.
    Per questo utilizziamo l'istanza current_userdi Flask-login .
    Il valore di current_user è l'oggetto restituito da user loader 
    """
    
    if current_user.is_authenticated:
        return redirect(url_for('projects'))



    #Creazione del modulo register form
    form = RegistrationForm()
     #Successivamente controlliamo se i dati inviati nel modulo sono validi. 
    if request.method == 'POST' and form.validate_on_submit():
        #Creo l'oggetto User partendo dai dati memorizzati nell'html con "form.attributo"


        user = UserModel(username=form.username.data.lower(), email=form.email.data.lower(), password=form.password.data)
        #Assegno la password all'utente
    
        #Permette di inserire una riga della tabella
        db.session.add(user)
        #permette di salvare la modifica sul database
        db.session.commit()
        flash('Congratulations, you are now a registered user!')

        #MODEL CORRISPONDE ALLA CLASSE DEL DATABASE
        #E' POSSIBILE OTTENERE TUTTE LE RIGHE CON  model.query.all ()
        

        #Reinderizzare con il link login
        return redirect(url_for('login'))

    elif request.method == 'GET':
    #mostrare il template con i dati del form
        return render_template('register.html', title='Register', form=form)



#PERCORSO DI LOGIN
@app.route('/login',  methods=['GET', 'POST'])
def login():
    nologin = False

    """
    Per prima cosa controlliamo se l'utente corrente è già autenticato.
    Per questo utilizziamo l'istanza current_userdi Flask-login .
    Il valore di current_user è l'oggetto restituito da user loader 
    """
    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    #Creazione del modulo login form
    form = LoginForm()
     #Successivamente controlliamo se i dati inviati nel modulo sono validi. 
    if request.method == 'POST' and form.validate_on_submit():
        
        # In tal caso, proviamo a recuperare l'utente dall'e-mail con query.filter_by sulla classe userModel
        user = UserModel.query.filter_by(email=form.email.data).first()
       
        #Controllo che l'oggetto utente non sia nullo e che la password corrisponda
        if user is None or user.password != form.password.data:
            nologin = True
            print("ciao mondo")
        else:
            # Se c'è un utente con quell'e-mail e la password corrisponde, procediamo all'autenticazione dell'utente chiamando il metodo login_user della classe Flask login.
            login_user(user, remember=form.remember_me.data)
            # Infine controlliamo se riceviamo il parametro next. Ciò accadrà quando l'utente ha tentato di accedere a una pagina protetta ma non è stato autenticato.
            # Per motivi di sicurezza, prenderemo in considerazione questo parametro solo se il percorso è relativo.
            # In questo modo evitiamo di reindirizzare l'utente verso un sito esterno al nostro dominio.
            #  Se il parametro successivo non viene ricevuto o non contiene un percorso relativo, reindirizziamo l'utente alla home page.
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('profile')
            return redirect(next_page)

    #restituzione del template html
    return render_template('login.html',  form=form, message=nologin)

 #CARICAMENTO DELL'UTENTE
@login_manager.user_loader
def load_user(id):
    return UserModel.query.get(int(id))

#PERCORSO DI LOGOUT
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


#PERCORSO DI LOGOUT
@app.route('/profile',methods=['GET', 'POST'])
def profile():
    
    form= FlaskForm()
    user= current_user
      #Gestione del tipo della richiesta
    if request.method == "POST":
        if request.form.get('modifyProfile') is not None:
            #Rendirizzamento al template task
            return redirect(url_for('edit_user', id_user= user.id))
        elif request.form.get('deleteProfile') is not None:
       #Rendirizzamento al template task
            return redirect(url_for('delete_user', id_user= user.id))
    elif request.method == "GET":
        return render_template('profile.html',  form= form)


    
#PERCORSO DI MODIFICA DEL TASK 
@app.route('/edit_user/<int:id_user>', methods=['GET', 'POST'])
@login_required #new line
def edit_user(id_user):
    #Acquisizione dell'oggetto user
    user = UserModel.query.get(int(id_user))

     #Creazione del form relativo al task 
    form1= RegistrationForm()
    if request.method == "POST":
        if request.form.get('modifyUser') is not None:
           
            if form1.password.data != form1.password2.data:
                 user.username= form1.username.data
                 user.email= form1.email.data
                 user.password= form1.password.data
                 db.session.commit()
                 return redirect(url_for('profile'))
    elif request.method == "GET":
        return render_template('edit_user.html', form =form1, user= user)



@app.route('/delete_user/<int:id_user>', methods=['POST'])
@login_required #new line
def delete_user(id_user):
    
    #Creazione del form relativo al task 
    current_user.remove()
    db.session.commit()
    flash('Your account has been successfully deleted. Hope to see you s.', 'success')
    return redirect(url_for('login'))