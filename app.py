from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()

db.init_app(app)
login_manager.init_app(app)

# view login
login_manager.login_view = 'login'
# Session <- conexão ativa

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/user', methods=['GET'])
def users():
  users = User.query.all()
  users_list = [{'id': user.id, 'username': user.username} for user in users]
  return jsonify(users_list), 200

@app.route('/user/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
  user = User.query.get(user_id)
  if user:
    return jsonify({'username': user.username})
  return jsonify({'message': 'Usuário não encontrado'}), 404

@app.route('/user/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
  data = request.json
  user = User.query.get(user_id)

  if user and data.get('password'):
    user.password = data.get('password')
    db.session.commit()
    return jsonify({'message': 'Usuário {user_id} atualizado com sucesso'})
  return jsonify({'message': 'Usuário não encontrado'}), 404
   
@app.route('/login', methods=['POST'])
def login():
  data = request.json
  username = data.get('username')
  password = data.get('password')

  if username and password:
    #login
    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        login_user(user)
        print(current_user.is_authenticated)
        return jsonify({'message': 'Autenticacao realizada com sucesso'}), 200

  return jsonify({'message': 'Credenciais inválidas'}), 400

@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return jsonify({'message': 'Logout realizado com sucesso'}), 200

@app.route('/user', methods=['POST'])
def create_user():
  data = request.json
  username = data.get("username")
  password = data.get("password")

  if username and password:
     user = User(username=username, password=password)
     db.session.add(user)
     db.session.commit()
     return jsonify({'message': 'Usuário criado com sucesso'}), 201
  
  return jsonify({'message': 'Dados inválidos'}), 400

@app.route('/hello-world', methods=['GET'])
def hello_world():
  return 'Hello World'

if __name__ == '__main__':
  app.run(debug=True)
