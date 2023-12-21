from flask import Flask, render_template
import random

app = Flask(__name__)

# Liste de mots pour l'exemple
mots = ["chat", "chien", "oiseau", "poisson", "lapin"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mot_aleatoire')
def mot_aleatoire():
    mot = random.choice(mots)
    return mot

@app.route('/lettre_aleatoire')
def lettre_aleatoire():
    mot = random.choice(mots)
    lettre = random.choice(mot)
    return lettre

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
