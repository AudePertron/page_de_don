# from pymongo import MongoClient

# #connexion à la bdd Atlas
# client = MongoClient('mongodb+srv://Aude:coucou@clusterdon.ngy1c.mongodb.net/sauver_rolistes?retryWrites=true&w=majority')
# db = client.sauver_rolistes
# donateurs = db.donateurs

# personDocument = {"nom": "machin", "prenom":"truc", "adresse":"4, rue des lilas 29200 Brest", "mail":"machin@truc.fr", "somme":1500, "conditions":1}

# donateurs.insert_one(personDocument)

##### test flask_pymongo
from flask import Flask
from flask_pymongo import pymongo

CONNECTION_STRING ='mongodb+srv://Aude:coucou@clusterdon.ngy1c.mongodb.net/sauver_rolistes?retryWrites=true&w=majority'
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('sauver_rolistes')
donateurs = db.donateurs

a = list(donateurs.aggregate([ {"$group": {"_id": "null","Total": {"$sum": "$somme"}}} ] ))
dons_tot = (a[0]['Total'])