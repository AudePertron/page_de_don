from flask import Flask, render_template, request, url_for, flash, redirect
import sqlite3
from werkzeug.exceptions import abort
from connexion import donateurs
from flask_user import login_required, UserManager, UserMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

#test authentification
# Flask-User settings
USER_APP_NAME = "Flask-User MongoDB App"      # Shown in and email templates and page footers
USER_ENABLE_EMAIL = False      # Disable email authentication
USER_ENABLE_USERNAME = True    # Enable username authentication
USER_REQUIRE_RETYPE_PASSWORD = False    # Simplify register form



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

@app.route('/liste', methods = ['GET'])
def liste():
    l_donateurs = donateurs.find({})
    a = list(donateurs.aggregate([ {"$group": {"_id": "null","Total": {"$sum": "$somme"}}} ] ))
    dons_tot = (a[0]['Total'])
    return render_template('liste.html', donateurs=l_donateurs, dons_tot=dons_tot)

@app.route('/merci')
def merci():
    return render_template('merci.html') 