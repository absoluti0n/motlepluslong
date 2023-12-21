from flask import Flask, render_template, request

app = Flask(__name__)


# Endpoint pour afficher le formulaire
@app.route('/')
def show_form():
    return render_template('input_form.html')


# Endpoint pour traiter l'input de l'utilisateur
@app.route('/process_input', methods=['POST'])
def process_input():
    user_input = request.form['user_input']
    return f'Vous avez saisi : {user_input}'


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
