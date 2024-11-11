from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return'<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])

def index():
    if request.method == 'POST':
        task_content = request.form.get('content', '').strip()
        if task_content:
            new_task = Todo(content=task_content)
            try: 
                db.session.add(new_task)
                db.session.commit()
            except:
                return 'There was an issue adding your task'
        return redirect('/')
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    print(f"Attempting to delete task with id: {id}")  

    try: 
        db.session.delete(task_to_delete)
        db.session.commit()
        print(f"Task with id: {id} deleted successfully")
        return redirect('/')
    except Exception as e:
        print(f"Error deleting task: {str(e)}") 
        return 'There was a problem deleting that task.'
    

    
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else: 
        return render_template('update.html', task=task)
    

@app.route('/view_all')
def view_all():
    tasks = Todo.query.all()
    return render_template('view_all.html', tasks=tasks)

    
if __name__ == "__main__":
    app.run(debug=True)
