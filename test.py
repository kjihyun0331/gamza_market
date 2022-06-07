from flask import Flask,render_template,request,flash,redirect,url_for,session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///User.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']="xinurocks"
app.config['UPLOAD_FOLDER'] = 'static/files'

db = SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True,autoincrement=True)
    userID=db.Column(db.String(20))
    userPW=db.Column(db.String(20))
    
    def __init__(self,id,pw):
        self.userID=id
        self.userPW=pw
        
class Following(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True,autoincrement=True)
    follower=db.Column(db.String(20))
    followee=db.Column(db.String(20))
    followeeID=db.Column(db.Integer)
    
    def __init__(self,follower,followee,id):
        self.follower=follower
        self.followee=followee
        self.followeeID=id
        
class products(db.Model):
    __tablename__ = 'products'
    
    title = db.Column(db.Integer, primary_key=True, unique = True, autoincrement=True)
    p_title = db.Column(db.String(50))
    p_price = db.Column(db.String(50))
    p_keyword1 = db.Column(db.String(30))
    p_keyword2 = db.Column(db.String(30), nullable=True)
    p_keyword3 = db.Column(db.String(30), nullable=True)
    p_description = db.Column(db.Text)
    p_state = db.Column(db.String(20))
    p_img = db.Column(db.String(50))
    
    def __init__(self, title, price, keyword1, description, state, img_file):
        self.p_title = title
        self.p_price = price
        self.p_keyword1 = keyword1
        self.p_description = description
        self.p_state = state
        self.p_img = img_file
        self.p_keyword2 = ""
        self.p_keyword3 = ""
        
        
@app.route('/')
def home():
    if 'username' in session:
        username = session['username']
        return render_template('homeLogin.html', username = username)
    else:
        return render_template('home.html')
    
@app.route('/Test')
def test():
    return render_template('test.html',User=User.query.all(),Following=Following.query.all())

@app.route('/delete/<user_id>')
def delete(user_id):
    user=User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return render_template('test.html',User=User.query.all())

@app.route('/Market')
def market():
    return render_template('market.html')

@app.route('/Mypage')
def mypage():
    if 'username' in session:
        username = session['username']
        return render_template('mypage.html', username = username,products=products.query.all())
    else:
        return redirect(url_for('login'))

@app.route('/Upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if not request.form['p_title'] or not request.form['p_price'] or not request.form['p_keyword1'] or not request.form['p_description'] or not request.form['p_state']:
            flash('Please enter all the fields', 'error')
        else:
            f = request.files['file']
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            
            product = products(request.form['p_title'], request.form['p_price'], request.form['p_keyword1'], request.form['p_description'], request.form['p_state'], secure_filename(f.filename))
            db.session.add(product)
            db.session.commit()
            
            return redirect(url_for('mypage'))
    return render_template('upload.html')

@app.route('/Update/<product_title>', methods = ['GET', 'POST'])
def update(product_title):
    update_product = products.query.filter_by(title = product_title).first()
    if request.method == 'POST':
        if not request.form['p_title'] or not request.form['p_price'] or not request.form['p_keyword1'] or not request.form['p_keyword2'] or not request.form['p_keyword3'] or not request.form['p_description'] or not request.form['p_state']:
            flash('모든 상품 정보를 입력해주세요.', 'error')
        else:
            update_product.p_title = request.form['p_title']
            update_product.p_price = request.form['p_price']
            update_product.p_keyword1 = request.form['p_keyword1']
            update_product.p_keyword2 = request.form['p_keyword2']
            update_product.p_keyword3 = request.form['p_keyword3']
            update_product.p_description = request.form['p_description']
            update_product.p_state = request.form['p_state']
            db.session.commit()
            
            return redirect(url_for('mypage'))
    return render_template('edit.html', product = update_product)

@app.route('/DeleteProduct/<product_title>')
def deleteProduct(product_title):
    product = products.query.filter_by(title = product_title).first()
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('mypage'))

@app.route('/Following')
def following():
    if 'username' in session:
        NowUser = Following.query.filter_by(follower=session['username']).all()
        return render_template('following.html', NowUser = NowUser,User=User.query.all())
    else:
        return redirect(url_for('login'))

@app.route('/Login', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        if not request.form['loginID'] or not request.form['loginPW']:
            flash('아이디 혹은 비밀번호를 입력하지 않으셨습니다.', 'error')
        else:
            loginID = request.form['loginID']
            loginPW = request.form['loginPW']
            data = User.query.filter_by(userID = loginID, userPW = loginPW).first()
            if data is not None:
                session['username'] = loginID
                return redirect(url_for('home'))
            else:
                flash('아이디 혹은 비밀번호 오류입니다.', 'error')
                return render_template('login.html')
    return render_template('login.html')

@app.route('/Signup_success')
def signup_success():
    return render_template('signupSuccess.html')

@app.route('/Signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        if not request.form['inputID'] or not request.form['inputPW']:
            flash('아이디 혹은 비밀번호를 입력하지 않으셨습니다.','error')
        else:
            inputID = request.form['inputID']
            data = User.query.filter_by(userID = inputID).first()
            if data is None:
                user=User(request.form['inputID'],request.form['inputPW'])
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('signup_success'))
            else:
                flash('이미 있는 아이디입니다.')
                return render_template('signup.html')
    return render_template('signup.html')

@app.route('/Logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/Shop/<user_id>')
def shop(user_id):
    Finduser=User.query.filter_by(id=user_id).first()
    if 'username' in session:
        nowUserFollowing=Following.query.filter_by(follower=session['username'],followee=Finduser.userID).first()
        followOrNot=nowUserFollowing is None
        return render_template('shop.html',FoN=followOrNot,user=Finduser)
    else:
        return render_template('shop.html',user=Finduser)

@app.route('/Follow/<user_id>')
def follow(user_id):
    if 'username' in session:
        newFollowee=User.query.filter_by(id=user_id).first()
        newFollow=Following(session['username'],newFollowee.userID,user_id)
        db.session.add(newFollow)
        db.session.commit()
        return redirect(url_for('following'))
    else:
        return render_template('login.html')
    
@app.route('/Unfollow/<user_id>')
def unfollow(user_id):
    removingFollowee=User.query.filter_by(id=user_id).first()
    removingFollow=Following.query.filter_by(follower=session['username'],followee=removingFollowee.userID).first()
    db.session.delete(removingFollow)
    db.session.commit()
    return redirect(url_for('following'))
    
if __name__=='__main__':
    db.create_all()
    app.run(debug=True)