#Importazione moduli necessari
import mimetypes
from this import d
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user, login_user, logout_user
from form import TaskForm, RegistrationForm, LoginForm, ProjectForm
from werkzeug.urls import url_parse
from datetime import datetime
from models import *
from flask import Flask, send_from_directory
from app import app
from werkzeug.utils import secure_filename
from sqlalchemy.orm import sessionmaker
from flask_wtf import FlaskForm
import os
import uuid


"""
Usiamo decoratori per definire percorsi URL nella nostra istanza dell'applicazione.
I percorsi URL possono includere variabili nelle loro definizioni consentendoci di personalizzare
 le nostre query per ottenere le informazioni esatte richieste.
 Per passare una variabile all'interno di una route si usa : <tipo:nome_variabile>.
 Per chiamare una funzione di route si usa la funzione : url_for('nome_funzione_route')

"""

#PERCORSO DI DEFAULT
@app.route('/')
def index():
  return redirect(url_for('login'))


"""

@app.before_first_request 
def create_user(): 
  db.session.add(UserModel(username= 'admin' , email='admin@libero.it', password='admin', is_admin= True))
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

    #mostrare il template con i dati del form
    return render_template('register.html', title='Register', form=form)


def save_image(picture_file):
    picture_name=picture_file.filename
    picture_path= os.path.join(app.root_path,'static/profile_pics',picture_name)
    picture_file.save(picture_path)
    return picture_name




#PERCORSO DI LOGIN
@app.route('/login', methods=['GET', 'POST'])
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
    if form.validate_on_submit():
        
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
            return redirect(url_for('delete', id_user= user.id))
    return render_template('profile.html',  form= form)


    
#PERCORSO DI MODIFICA DEL TASK 
@app.route('/<int:id_user>/edit_user', methods=['GET', 'POST'])
@login_required #new line
def edit_user(id_user):
    #Acquisizione dell'oggetto user
    user = UserModel.query.get(int(id_user))

     #Creazione del form relativo al task 
    form1= RegistrationForm()
    if request.method == "POST":
        if request.form.get('modifyUser') is not None:
            print("ehilaaaa")
            user.username= form1.username.data
            user.email= form1.email.data
            user.password= form1.password.data
            db.session.commit()
            return redirect(url_for('profile'))
    
    return render_template('edit_user.html', form =form1, user= user)



@app.route('/<int:id_user>/delete', methods=['GET', 'POST'])
@login_required #new line
def delete(id_user):
    
    #Creazione del form relativo al task 
    current_user.remove()
    db.session.commit()
    flash('Your account has been successfully deleted. Hope to see you s.', 'success')
    return redirect(url_for('login'))


"""Route gestione progetti"""
@app.route('/menu_project', methods=['GET', 'POST'])
@login_required #new line
def projects():                   
    #Restituisco il template share.html
    return render_template('menu_projects.html',title='Request Project')    

 #PERCORSO DI CREAZIONE DEL TASK
@app.route('/create-project', methods=['GET', 'POST'])
@login_required #new line
def create_project():

    #Acquisizione dell'oggetto user
    user = current_user
    
    project = Project.query.filter(Project.author.any(id= user.id)).all()
    print(project)
   
  
  
    #Creazione del form relativo al task 
    form= ProjectForm()

    #Gestione del tipo della richiesta
    if request.method == "POST":

    #Gestione del click sul bottone aggiungi 
        if request.form.get('projectAdd') is not None:


                #Creazione dell'oggetto Todo
                f = request.files['file']
                print(f)

                filename = secure_filename(f.filename)
                image_file= save_image(f)
                uuidOne = uuid.uuid1()

                #Creazione dell'oggetto progetto
                project_item = Project(id=str(uuidOne),  title=form.title.data,description= form.description.data, image= image_file,mimetype=f.mimetype, created_by=user.id) #new line
                #Aggiunta del progetto all'utente
                user.projects.append(project_item)

                db.session.add(project_item)
                db.session.commit()
             
                return redirect(url_for('projects'))

    #Rendirizzamento al template task
    return render_template('create_project.html', title='Create Project', form=form) 



 #PERCORSO DI CREAZIONE DEL TASK
@app.route('/show-my-projects', methods=['GET', 'POST'])
@login_required #new line
def show_my_projects():
     #Acquisizione dell'oggetto user
    user = current_user
    
    projects = Project.query.filter(Project.author.any(id= user.id)).all()
    print(projects)
       #Creazione del form relativo al task 
    form= FlaskForm()

      #Gestione del tipo della richiesta
    if request.method == "POST":

            #Gestione del click sul tasto delete del item
        if request.form.get('showTask') is not None:
                
            #Filtrare l'id del progettos
            id_project=request.form.get('showTask')
            
            #Restituzione del template tasks
            return redirect(url_for('create_task', id_project= id_project))

         #Gestione del click sul tasto delete del item
        elif request.form.get('shareTask') is not None:
            
            #Filtrare l'id del progettos
            id_project=request.form.get('shareTask')
            
            #Restituzione del template tasks
            return redirect(url_for('share_project',id_user = user.id,id_project= id_project))

    return render_template('show_my_projects.html',form=form, projects= projects) 




 #PERCORSO DI CREAZIONE DEL TASK
@app.route('/show-others-projects', methods=['GET', 'POST'])
@login_required #new line
def show_others_projects():
     #Acquisizione dell'oggetto user
    user = current_user
    projects_me= Project.query.filter(Project.author.any(id= user.id)).all()
    print("ehi"+ str(projects_me))
    projects_all= Project.query.filter().all()
    associations = Association.query.filter_by(user_id_mittente= current_user.id).all()
    projects= [project for project in projects_all if project not in projects_me]
    project_not_requested= []
    for project in projects:
        flag= False
        for association in associations:
            if project.id== association.project_id:
                flag= True
        if flag== False:
            project_not_requested.append(project)
    print(project_not_requested)        
  
       #Creazione del form relativo al task 
    form= FlaskForm()
      #Gestione del tipo della richiesta
    if request.method == "POST":

         #Gestione del click sul tasto delete del item
        if  request.form.get('requestTask') is not None:
            
            #Filtrare l'id del progettos
            id_project=request.form.get('requestTask')
            project = Project.query.filter_by(id=id_project).one()
            association = Association(user_id_destinatario= project.created_by)
            association.project=project
          
            user.requests.append(association)
            db.session.add(association)
            db.session.commit()
            return redirect(url_for('show_others_projects'))


    return render_template('show_others_projects.html',form=form, projects= project_not_requested) 






    #PERCORSO DI MODIFICA DEL TASK 
@app.route('/<int:id_user>/<string:id_project>/share-project', methods=['GET', 'POST'])
@login_required #new line
def share_project(id_user, id_project):
    
    
    #Creazione del form relativo al task 
    form= TaskForm()
    #Ottengo la la lista degli utenti diversi dall'utente originale
    users= UserModel.query.filter(UserModel.id != id_user).all()
    #Mi ottengo tutta la lista dei progetti dell'utente
    #mi ottengo il progetto di riferimento
    project = Project.query.filter_by(id= id_project).one()

    []
    users_reducted= []
    for user in users:
        print(user)
        projects = Project.query.filter(Project.author.any(id= user.id)).all()
        if project not in projects:
            users_reducted.append(user)

    if(request.form.get('projectShare') is not None):
                project = Project.query.filter_by(id=id_project).one()
                user =  UserModel.query.filter_by(id=request.form.get('projectShare')).one()
                user.projects.append(project)
                db.session.commit()
                return redirect(url_for('share_project',id_user = user.id,id_project= id_project))

    #Restituisco il template share.html
    return render_template('share_project.html', users= users_reducted, form = form) 

"""Route per gestione richieste"""

@app.route('/requests', methods=['GET', 'POST'])
@login_required #new line
def requests():                   
    #Restituisco il template share.html
    return render_template('menu_request.html') 


 

@app.route('/request_received', methods=['GET', 'POST'])
@login_required #new line
def request_received():
       
    user= current_user
    user_requests= Association.query.filter_by(user_id_destinatario= user.id).all()
    user_requests= [user_request for user_request in user_requests if user_request.accepted== False and  user_request.refused== False ]
    requests=[]
    i=0
    for user_request in user_requests: 
        project=  Project.query.filter_by(id=user_request.project_id).one()
        user= UserModel.query.filter_by(id= user_request.user_id_mittente).one()
        requestt= Request(i ,project.id, project.title,user.id, user.username, user.email,user_request.accepted,user_request.refused)
        i=i +1
        requests.append(requestt)
    print(requests)
    #Creazione del form relativo al task 
    form= TaskForm()

       #Gestione del tipo della richiesta
    if request.method == "POST":

         #Gestione del click sul tasto delete del item
        if  request.form.get('acceptRequest') is not None:
        
            #Filtrare l'id del progettos
            id_request=int(request.form.get('acceptRequest'))
        
            
            for richiesta in requests:
                id= richiesta.id
              
                if id == id_request:
                    print("HEY")
                    dati_richiesta= richiesta
                    id_progetto= dati_richiesta.id_progetto
                    id_utente= dati_richiesta.id_mittente
                    for rquest in user_requests:
                        if rquest.project_id== id_progetto and rquest.user_id_destinatario:
                            rquest.accepted=True
                    project = Project.query.filter_by(id=id_progetto).one()
                    user =  UserModel.query.filter_by(id=id_utente).one()
                    user.projects.append(project)
                    db.session.commit()
                    return redirect(url_for('requests'))

                    
         
        #Gestione del click sul tasto delete del item
        elif  request.form.get('rejectRequest') is not None:
             #Filtrare l'id del progettos
            id_request=int(request.form.get('rejectRequest'))
        
            
            for richiesta in requests:
                id= richiesta.id
              
                if id == id_request:
                    print("HEY")
                    dati_richiesta= richiesta
                    id_progetto= dati_richiesta.id_progetto
                    id_utente= dati_richiesta.id_mittente
                    for rquest in user_requests:
                        if rquest.project_id== id_progetto and rquest.user_id_destinatario:
                            rquest.refused=True
                    db.session.commit()
                    

                    return redirect(url_for('requests'))

                   
    #Restituisco il template share.html
    return render_template('request_received.html', requests= requests, form = form) 
    
    
@app.route('/request_done')
@login_required #new line
def request_done():
       
    user= current_user
    user_requests= Association.query.filter_by(user_id_mittente= user.id).all()
    requests=[]
    i=0
    for user_request in user_requests: 
        project=  Project.query.filter_by(id=user_request.project_id).one()
        user= UserModel.query.filter_by(id= user_request.user_id_mittente).one()
        requestt= Request(i ,project.id, project.title,user.id, user.username, user.email,user_request.accepted, user_request.refused)
        i=i +1
        requests.append(requestt)

    print(requests)              
    #Restituisco il template share.html
    return render_template('request_done.html', requests= requests) 

 
#PERCORSO DI CREAZIONE DEL TASK
@app.route('/<string:id_project>/create-task', methods=['GET', 'POST'])
@login_required #new line
def create_task(id_project):

    #Acquisizione dell'oggetto user
    user = current_user
    
    #Filtrare tutti i gli oggetti todo dell'utente
    todo= Task.query.filter_by(project_id=id_project) #new line
    todo= [todo_item for todo_item in todo if todo_item.checked == False]
    #Acquisizione della data corrente
    date= datetime.now()
    now= date.strftime("%Y-%m-%d")

    #Creazione del form relativo al task 
    form= TaskForm()

    #Gestione del tipo della richiesta
    if request.method == "POST":

        #Gestione del click sul tasto delete del item
        if request.form.get('taskDelete') is not None:
            
            #Filtrare l'item con l'id associato al bottone taskDelete come "value"
            todo_item = Task.query.filter_by(id=request.form.get('taskDelete')).one()
            
            #Eliminare l'item filtrato
            db.session.delete(todo_item)

            #Applicazione della modifica al database
            db.session.commit()

            #Restituzione del template tasks
            return redirect(url_for('create_task',id_project= id_project ))

           
        elif request.form.get('taskModify') is not None:
            
            #Filtrare l'item con l'id associato al bottone taskModifycome "value"
            id =request.form.get('taskModify')
            
            #chiamata della route id
            return redirect(url_for('edit_tasks', id_project= id_project, id_task= id))

    


            #Gestione del click sul bottone aggiungi 
        elif request.form.get('taskAdd') is not None:

                #Ottenere la categoria inserita nel template
                selected=  request.form.get('category')

                #ottenere l'oggetto categoria
                category= Category.query.filter_by(id=selected).one()
                project = Project.query.filter_by(id=id_project).one()
                #Creazione dell'oggetto Todo
                todo_item = Task(title=form.title.data, date=form.date.data, time= form.time.data, category= category.name, project_id=project.id) #new line
                db.session.add(todo_item)
                db.session.commit()
                return redirect(url_for('create_task',id_project= id_project))


    #Rendirizzamento al template task
    return render_template('create_task.html', title='Create Tasks', form=form, todo=todo, DateNow=now)


#PERCORSO DI MODIFICA DEL TASK 
@app.route('/<string:id_project>/<int:id_task>/edit_tasks', methods=['GET', 'POST'])
@login_required #new line
def edit_tasks(id_project,id_task):
    #Acquisizione dell'oggetto user


     #Filtrare tutti i gli oggetti todo dell'utente
    #Filtrare l'item con l'id associato al bottone taskDelete come "value"
    todo_item = Task.query.filter_by(id=id_task).one()
    project = Project.query.filter_by(id=id_project).one()
    print(str(todo_item))
  
     #Creazione del form relativo al task 
    form1= TaskForm()

    #Gestione del tipo della richiesta
    if request.method == "POST":
        print(request.form.get('taskModify'))
        if request.form.get('taskModify') is not None:

                #Ottenere la categoria inserita nel template
                selected= form1.category.data


                #ottenere l'oggetto categoria
                category= Category.query.get(selected)
                #Creazione dell'oggetto Todo
                todo_item_new = Task(title=form1.title.data, date=form1.date.data, time= form1.time.data, category=category.name, author=project) #new line
                db.session.delete(todo_item)
                db.session.commit()

                #Applicare modifica al db                
                db.session.add(todo_item_new)
                db.session.commit()
                flash('Congratulations, you just added a new note')
                return redirect(url_for('create_task', id_project= id_project))
    #Rendirizzamento al template task
    return render_template('edit_task.html', title='Modify Tasks', form=form1, todo=todo_item)




 
     
