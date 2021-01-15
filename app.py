from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort
from connexion import donateurs, membres

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/form_don', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        nom =request.values.get('nom_donneur')
        prenom = request.values.get('prenom_donneur')
        adresse = request.values.get('adresse_donneur')
        mail = request.values.get('mail_donneur')
        somme = int(request.values.get('somme'))
        conditions = request.values.get('conditions')
        if not conditions:
            flash('Merci de valider les conditions générales !')
        else:
            donateurs.insert_one({"nom": nom, "prenom": prenom, "adresse":adresse, "mail":mail, "somme":somme})
            return redirect(url_for('merci'))

    return render_template('form_don.html')

@app.route('/form_don')
def form_don():
    return render_template('form_don.html') 

@app.route('/chanson')
def chanson():
    return render_template('chanson.html') 

@app.route('/login', methods = ('GET', 'POST'))
def login():
    login = membres.find({})
    b=(list(membres.find({})))
    password = (b[0]['password'])
    login = (b[0]['login'])
    log_user =request.values.get('login')
    pass_user = request.values.get('password')

    if log_user == login and pass_user == password:        
        l_donateurs = donateurs.find({})
        a = list(donateurs.aggregate([ {"$group": {"_id": "null","Total": {"$sum": "$somme"}}} ] ))
        dons_tot = (a[0]['Total'])
        return render_template('liste.html', donateurs=l_donateurs, dons_tot=dons_tot)      
    else :
        return render_template('login.html')
@app.route('/liste', methods = ['GET'])
#@login_required
def liste():
    l_donateurs = donateurs.find({})
    a = list(donateurs.aggregate([ {"$group": {"_id": "null","Total": {"$sum": "$somme"}}} ] ))
    dons_tot = (a[0]['Total'])
    return render_template('liste.html', donateurs=l_donateurs, dons_tot=dons_tot)

@app.route('/merci')
def merci():
    return render_template('merci.html')