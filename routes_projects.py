
#Importazione moduli necessari
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from form import TaskForm, ProjectForm
from datetime import datetime
from models import *
from app import app
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
import uuid
import os


"""Route gestione progetti"""
@app.route('/projects/<int:id_user>', methods=['GET'])
@login_required #new line
def projects(id_user):      
    
    user = UserModel.query.filter_by(id=id_user).one()             
    #Restituisco il template share.html
    return render_template('menu_projects.html',title='Request Project')    




def save_image(picture_file):
    picture_name=picture_file.filename
    picture_path= os.path.join(app.root_path,'static/profile_pics',picture_name)
    picture_file.save(picture_path)
    return picture_name


 #PERCORSO DI CREAZIONE DEL TASK
@app.route('/projects/<int:id_user>/create', methods=['GET', 'POST'])
@login_required #new line
def create_project(id_user):

    #Acquisizione dell'oggetto user
    user = UserModel.query.filter_by(id=id_user).one()
    

  
    #Creazione del form relativo al task 
    form= ProjectForm()

    #Gestione del tipo della richiesta
    if request.method == "POST":

    #Gestione del click sul bottone aggiungi 
        if request.form.get('projectAdd') is not None:


                #Creazione dell'oggetto Todo
                f = request.files['file']
                image_file= save_image(f)
                uuidOne = uuid.uuid1()

                #Creazione dell'oggetto progetto
                project_item = Project(id=str(uuidOne),  title=form.title.data,description= form.description.data, image= image_file,mimetype=f.mimetype, created_by=user.id) #new line
                #Aggiunta del progetto all'utente
                user.projects.append(project_item)

                db.session.add(project_item)
                db.session.commit()
             
                return redirect(url_for('projects', id_user= current_user.id))

    #Gestione del tipo della richiesta
    elif request.method == "GET":
    #Rendirizzamento al template task
        return render_template('create_project.html', title='Create Project', form=form) 



 #PERCORSO DI CREAZIONE DEL TASK
@app.route('/projects/<int:id_user>/my_projects', methods=['GET', 'POST'])
@login_required #new line
def show_my_projects(id_user):
     #Acquisizione dell'oggetto user
    user = UserModel.query.filter_by(id=id_user).one()
    
    projects = Project.query.filter(Project.author.any(id= user.id)).all()
       #Creazione del form relativo al task 
    form= FlaskForm()

      #Gestione del tipo della richiesta
    if request.method == "POST":

            #Gestione del click sul tasto delete del item
        if request.form.get('showTask') is not None:
                
            #Filtrare l'id del progettos
            id_project=request.form.get('showTask')
            
            #Restituzione del template tasks
            return redirect(url_for('create_task', id_user = user.id,id_project= id_project))

         #Gestione del click sul tasto delete del item
        elif request.form.get('shareTask') is not None:
            
            #Filtrare l'id del progettos
            id_project=request.form.get('shareTask')
            
            #Restituzione del template tasks
            return redirect(url_for('share_project',id_user = user.id,id_project= id_project))

    #Gestione del tipo della richiesta
    elif request.method == "GET":
            return render_template('show_my_projects.html',form=form, projects= projects) 




 #PERCORSO DI CREAZIONE DEL TASK
@app.route('/projects/<int:id_user>/other_projects', methods=['GET', 'POST'])
@login_required #new line§é09uy 
def show_others_projects(id_user):
     #Acquisizione dell'oggetto user
    user = UserModel.query.filter_by(id=id_user).one()
    projects_me= Project.query.filter(Project.author.any(id= user.id)).all()
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
            return redirect(url_for('projects', id_user= current_user.id))

    #Gestione del tipo della richiesta
    elif request.method == "GET":

        return render_template('show_others_projects.html',form=form, projects= project_not_requested) 






    #PERCORSO DI MODIFICA DEL TASK 
@app.route('/projects/<int:id_user>/my_projects/<string:id_project>/share_project/', methods=['GET', 'POST'])
@login_required #new line
def share_project(id_user, id_project):
    
    user = UserModel.query.filter_by(id=id_user).one()
    #Creazione del form relativo al task 
    form= TaskForm()
    #Ottengo la la lista degli utenti diversi dall'utente originale
    users= UserModel.query.filter(UserModel.id != id_user).all()
    #Mi ottengo tutta la lista dei progetti dell'utente
    #mi ottengo il progetto di riferimento
    project = Project.query.filter_by(id= id_project).one()
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
                return redirect(url_for('projects',id_user = user.id,id_project= id_project))


    #Gestione del tipo della richiesta
    elif request.method == "GET":
    #Restituisco il template share.html
                return render_template('share_project.html', users= users_reducted, form = form) 


     
#PERCORSO DI CREAZIONE DEL TASK
@app.route('/projects/<int:id_user>/my_projects/<string:id_project>/create_task', methods=['GET', 'POST'])
@login_required #new line
def create_task(id_user,id_project):

    #Acquisizione dell'oggetto user
     
    user = UserModel.query.filter_by(id=id_user).one()
    
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
            return redirect(url_for('create_task',id_user = user.id,id_project= id_project ))

           
        elif request.form.get('taskModify') is not None:
            
            #Filtrare l'item con l'id associato al bottone taskModifycome "value"
            id =request.form.get('taskModify')
            
            #chiamata della route id
            return redirect(url_for('edit_task', id_user = user.id,id_project= id_project, id_task= id))

    


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
                return redirect(url_for('projects', id_user= current_user.id))

  #Gestione del tipo della richiesta
    elif request.method == "GET":
        #Rendirizzamento al template task
        return render_template('create_task.html', title='Create Tasks', form=form, todo=todo, DateNow=now)


#PERCORSO DI MODIFICA DEL TASK 
@app.route('/projects/<int:id_user>/my_projects/<string:id_project>/edit_task/<int:id_task>', methods=['GET', 'POST'])
@login_required #new line
def edit_task(id_user,id_project,id_task):
    #Acquisizione dell'oggetto user

    user = UserModel.query.filter_by(id=id_user).one()
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
                return redirect(url_for('create_task', id_user = user.id, id_project= id_project))
                  #Gestione del tipo della richiesta
    elif request.method == "GET":
    #Rendirizzamento al template task
            return render_template('edit_task.html', title='Modify Tasks', form=form1, todo=todo_item)
