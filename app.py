from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tasks.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

class Todo (db.Model):
    sno= db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    desc=db.Column(db.String(500), nullable=False)
    date_created=db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"


@app.route('/', methods=['GET','POST'])
def hell_world():
    if request.method=='POST':
        title = request.form['title']
        desc=request.form['desc']
        todo= Todo(title=title,desc=desc)
        db.session.add(todo)
        db.session.commit()
    
    allTodo=Todo.query.all()
    return render_template('index.html',alltodo=allTodo)

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc=request.form['desc']
        upTodo = Todo.query.filter_by(sno=sno).first()
        upTodo.title=title
        upTodo.desc=desc
        db.session.add(upTodo)
        db.session.commit()
        return redirect('/')

    upTodo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=upTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    delTodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(delTodo)
    db.session.commit()
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True, port=3000)