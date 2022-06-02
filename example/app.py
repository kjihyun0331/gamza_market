from flask import Flask,request,flash,redirect,render_template,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']="xinurocks"

db = SQLAlchemy(app)

class students(db.Model):
    id=db.Column(db.Integer,primary_key=True,unique=True,autoincrement=True)
    s_id=db.Column(db.String(30))
    s_name=db.Column(db.String(100))
    
    def __init__(self,id,name):
        self.s_id=id
        self.s_name=name
        
@app.route('/add_new',methods=['GET','POST'])
def add_new():
    if request.method=='POST':
        if not request.form['s_id'] or not request.form['s_name']:
            flash('Please enter all the fields','error')
        else:
            student=students(request.form['s_id'],request.form['s_name'])
            db.session.add(student)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('show_all'))
    return render_template('add_new.html')

@app.route('/show_all')
def show_all():
    return render_template('show_all.html',students=students.query.all())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/delete/<student_id>')
def delete(student_id):
    student=students.query.filter_by(id=student_id).first()
    db.session.delete(student)
    db.session.commit()
    return render_template('show_all.html',students=students.query.all())

@app.route('/update/<student_id>',methods=['GET','POST'])
def update(student_id):
    update_student=students.query.filter_by(id=student_id).first()
    if request.method=='POST':
        if not request.form['s_id'] or not request.form['s_name']:
            flash('Please enter all the fields','error')
        else:
            update_student.s_id=request.form['s_id']
            update_student.s_name=request.form['s_name']
            db.session.commit()
            
            flash('Record was successfully updated')
            return redirect(url_for('show_all'))
    return render_template('edit.html',student=update_student)

if __name__=='__main__':
    db.create_all()
    app.run(debug=True)