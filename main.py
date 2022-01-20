# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


"""def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/"""


from flask import Flask , render_template,request,redirect
from flask_mongoengine import MongoEngine
from datetime import datetime
app=Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'task_manager_app',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)
class task_manager (db.Document):
    task_id=db.IntField(primary_key=True)
    task_name=db.StringField()
    date_of_creation=db.DateTimeField()
    date_of_completion=db.DateTimeField(required=True)
    completed=db.BooleanField(default=True)

@app.route('/',methods=['POST','GET'])

def load():
    if request.method=="POST":
        try:
            created_date=(request.form['created'])
        except:
            created_date=(datetime.now())
        completion_date=(request.form['completed'])

        complet=request.form['status']
        task_id=request.form['task_id']
        task=request.form['content']
        boo=True
        if complet=="No":
            boo=False

        try:
            user=task_manager(task_id=int(task_id), task_name=str(task), date_of_creation=created_date, date_of_completion=completion_date, completed=boo)
            user.save()
            return redirect('/')
        except():
            return "Ooops Something gone wrong.Try Again"

    else:
        tasks=task_manager.objects().all()
        return render_template("home.html",tasks=tasks)
@app.route('/delete/<id>')
def delete(id):
    task=task_manager.objects(task_id=id).all()
    task.delete()
    return redirect('/')
@app.route('/update/<id>',methods=['POST','GET'])
def update(id):
    task = task_manager.objects(task_id=id).first()
    if request.method=="POST":
        t_id=request.form['task_id']
        t_name=request.form['content']
        t_c=request.form['created']
        t_cd=request.form['completed']
        t=str(task.date_of_creation)
        t1=str(t_c)
        t1=t1.strip()
        t=t[:11]
        t=t.strip()
        if t!=t1:
            return "<h1 style='font_size=200%'>Date of Creation cannot be changed</h1>"
        try:
            t_s=request.form['status']
        except:
            t_s=task.completed
        boo=False
        if t_s=="Yes":
            boo=True

        task.update(task_name=t_name,date_of_creation=t_c,date_of_completion=t_cd,completed=boo)
        return redirect('/')
    else:

        return render_template("update.html",task=task)
@app.route('/search',methods=['POST','GET'])
def search():
    if request.method=="POST":
        attribute=request.form['searchby']
        attribute=attribute.strip()
        #return (str(list(attribute)))
        value=request.form['search']
        if attribute=="task_id":
            match = task_manager.objects(task_id=value).all()
        elif attribute=="task_name":
            match = task_manager.objects(task_name=value).all()
        elif attribute=="date_of_creation":
            value+=" 00.00.00"
            match = task_manager.objects(date_of_creation=value).all()
        elif attribute=="date_of_completion":
            value+=" 00.00.00"
            match=task_manager.objects(date_of_completion=value).all()
        else:
            if value=="True":
                value=True
            else:
                value=False
            match = task_manager.objects(completed=value).all()
        return render_template("result.html",match=match)
    else:
        return render_template("search.html")






