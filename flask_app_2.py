from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

@app.route('/')
def home():
    return render_template('ask_name.html')

@app.route('/display', methods=['POST'])
def display():
    name = request.form['name']
    user = User(name=name)
    db.session.add(user)
    db.session.commit()
    return render_template('display_name.html', name=name)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # create tables
    app.run(debug=True)
