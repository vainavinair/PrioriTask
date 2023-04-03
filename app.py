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
    due_date=db.Column(db.DateTime, nullable=True)




@app.route('/', methods=['GET','POST'])
def hell_world():
    if request.method=='POST':
        title = request.form['title']
        desc=request.form['desc']
        due_date_str=request.form['due']
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        todo= Todo(title=title,desc=desc,due_date= due_date)
        db.session.add(todo)
        db.session.commit()
    
    all_todo=Todo.query.all()
    return render_template('index.html',alltodo=all_todo)

@app.route('/update/<int:sno>', methods=['GET','POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc=request.form['desc']
        due_date_str=request.form['due']
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        up_todo = Todo.query.filter_by(sno=sno).first()
        up_todo.title=title
        up_todo.desc=desc
        up_todo.due_date=due_date
        db.session.add(up_todo)
        db.session.commit()
        return redirect('/')

    up_todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html',todo=up_todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    delTodo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(delTodo)
    db.session.commit()
    return redirect('/')

@app.route('/about')
def about():
    return render_template('about.html')


if __name__=="__main__":
    app.run(debug=True, port=3000)