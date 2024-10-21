import flask
from flask import jsonify, request, render_template, redirect, url_for, session, flash

app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = 'votre_clé_secrète'  # Nécessaire pour gérer les sessions

# Liste des utilisateurs fictifs
users = [
    {'id': 0, 'pseudo': 'jeandupont', 'mdp': 'jeannot123'},
    {'id': 1, 'pseudo': 'test', 'mdp': 'test'},
    {'id': 2, 'pseudo': 'admin', 'mdp': 'admin'}
]

# Page d'accueil avec des liens vers la connexion et l'inscription
@app.route('/')
def index():
    return render_template('index.html')

# Route pour afficher la page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pseudo = request.form['pseudo']
        mdp = request.form['mdp']

        # Vérification des identifiants
        for user in users:
            if user['pseudo'] == pseudo and user['mdp'] == mdp:
                session['user'] = user['pseudo']  # Définir la session utilisateur
                flash('Connexion réussie!', 'success')
                return redirect(url_for('dashboard'))

        # Si les identifiants ne correspondent pas
        flash('Identifiants invalides', 'danger')
    
    return render_template('login.html')

# Route pour afficher la page d'inscription (ajouter un utilisateur)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        pseudo = request.form['pseudo']
        mdp = request.form['mdp']

        # Ajouter un nouvel utilisateur
        new_user = {
            'id': len(users),
            'pseudo': pseudo,
            'mdp': mdp
        }
        users.append(new_user)
        flash('Inscription réussie! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Route pour le tableau de bord après connexion
@app.route('/dashboard')
def dashboard():
    if 'user' in session:  # Vérifie si l'utilisateur est connecté
        return f'<h1>Bienvenue {session["user"]}!</h1><a href="/logout">Se déconnecter</a>'
    else:
        flash('Vous devez vous connecter pour accéder au tableau de bord', 'warning')
        return redirect(url_for('login'))

# Route pour déconnecter l'utilisateur
@app.route('/logout')
def logout():
    session.pop('user', None)  # Supprime la session utilisateur
    flash('Vous vous êtes déconnecté.', 'info')
    return redirect(url_for('login'))

# Page pour lister tous les utilisateurs
@app.route('/users')
def list_users():
    return render_template('users.html', users=users)

# Lancer l'application Flask
if __name__ == '__main__':
    app.run()
