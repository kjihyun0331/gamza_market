from flask import Flask,render_template,request,flash,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///User.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']="xinurocks"

db = SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True,autoincrement=True)
    userID=db.Column(db.String(20))
    userPW=db.Column(db.String(20))
    
    def __init__(self,id,pw):
        self.userID=id
        self.userPW=pw

@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        return render_template('homeLogin.html', username = username)
    else:
        return render_template('home.html')
    
@app.route('/Test')
def test():
    return render_template('test.html',User=User.query.all())

@app.route('/Market')
def market():
    return render_template('market.html')

@app.route('/Mypage')
def mypage():
    return render_template('mypage.html')

@app.route('/Upload')
def upload():
    return render_template('upload.html')

@app.route('/Following')
def following():
    return render_template('following.html')

@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        if not request.form['loginID'] or not request.form['loginPW']:
            flash('Please enter all the fields', 'error')
        else:
            loginID = request.form['loginID']
            loginPW = request.form['loginPW']
            data = User.query.filter_by(userID = loginID, userPW = loginPW).first()
            if data is not None:
                session['username'] = loginID
                return redirect(url_for('home'))
            else:
                return render_template('login.html')
    return render_template('login.html')

@app.route('/Signup_success')
def signup_success():
    return render_template('signupSuccess.html')

@app.route('/Signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        if not request.form['inputID'] or not request.form['inputPW']:
            flash('Please enter all the fields','error')
        else:
            user=User(request.form['inputID'],request.form['inputPW'])
            db.session.add(user)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('signup_success'))
    return render_template('signup.html')

if __name__=='__main__':
    db.create_all()
    app.run(debug=True)