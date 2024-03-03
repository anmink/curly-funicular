from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, request, jsonify
import http.client
import json

app = Flask(__name__)

uri = "mongodb+srv://admin:QJsXw6u9rtW6u0hx@cluster0.xcihtjj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri, server_api=ServerApi('1'))
client.admin.command('ping')
print('MongoDB connected...')

db = client['smartdress_db']
collection_imageParamter = db['imageParameter']
collection_user = db['user']

test_data = {
    "userId": "anne94",
    "img": "xxxBase64Code",
    "clothingType": "tshirt",
    "color": ["blue", "white"],
    "reason": ["casual", "sporty"],
    "season": ["spring"]
}

@app.route('/', methods=['GET'])
def get_data():
    data = collection_imageParamter.find()  # Daten aus der MongoDB abrufen
    result = []  # Leere Liste für die Ergebnisse initialisieren
    for d in data:
        result.append({
            'type': d['type'],    
            'color': d['color'],
            'season': d['season'],
            'reason': d['reason'],
            'image': d['image']
        })
    return jsonify({'data': result})  # Daten als JSON zurückgeben

@app.route('/put', methods=['POST'])
def saveParameters():
    data = request.json
    """ required_fields = ['userId', 'img', 'color']
    if not all(field in data for field in required_fields):
        return jsonify(message='Fehlende Daten, bitte stelle sicher, dass userId, img und color übermittelt werden.'), 400 """
    collection_imageParamter.insert_one(data)
    return jsonify(message='Daten erfolgreich gespeichert'), 201

if __name__ == '__main__':
    print('hi')
    app.run(debug=True)
