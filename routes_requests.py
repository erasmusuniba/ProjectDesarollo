#Importazione moduli necessari
import mimetypes
from this import d
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user, login_user, logout_user
from form import TaskForm, RegistrationForm, LoginForm, ProjectForm

from models import *
from app import app


"""Route per gestione richieste"""

@app.route('/requests/<int:id_user>')
@login_required #new line
def requests(id_user):                   
    #Restituisco il template share.html
    return render_template('menu_request.html') 


 

@app.route('/requests/<int:id_user>/received', methods=['GET', 'POST'])
@login_required #new line
def requests_received(id_user):
       
    user = UserModel.query.filter_by(id=id_user).one()   
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
                    return redirect(url_for('requests',id_user= user.id))

                    
         
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
                    

                    return redirect(url_for('requests', id= user.id))

                   
    #Restituisco il template share.html
    return render_template('request_received.html', requests= requests, form = form) 
    
    
@app.route('/requests/<int:id_user>/done')
@login_required #new line
def requests_done(id_user):
       
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


