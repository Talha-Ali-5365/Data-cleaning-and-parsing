from flask import Flask, render_template, redirect,url_for,request

app = Flask(__name__)
print(__name__)

@app.route('/')
def home():
    return render_template('index2.html')
@app.route('/submit', methods=['GET','POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        print(f'Submitted name: {name}')
        return redirect(url_for('result', name=name))
@app.route('/result/<name>')
def result(name):
    return render_template('result.html', name=name)

if __name__ == '__main__':
    app.run(debug=True)