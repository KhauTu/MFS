from flask import *
from models.service import Item, Category, User
import mlab
import os
from werkzeug.utils import secure_filename

mlab.connect()

app = Flask(__name__)

UPLOAD_FOLDER = "static/media/"
ALLOWED_EXTENSIONS = set(['txt', 'jpg', 'php', 'png', 'gif', 'jpeg'])

app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

def allowed_file(filename):
    check_1 = "." in filename
    check_2 = filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    return check_1 and check_2

def savefile(file ,file_name):
    if file and allowed_file(file_name):
        file_name = secure_filename(file_name)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        print("Saved")
    return file_name

@app.route('/')
def homepage():
    all_items = Item.objects()
    return render_template('homepage.html', all_items = all_items)

@app.route('/sign-up', methods = ['GET','POST'])
def sign_up():
    if request.method == "GET":
        return render_template('homepage/sign-up.html')
    elif request.method == "POST":

        form = request.form
        user_name = form['user_name']
        password = form['password']
        email = form['email']
        phone = form['phone']

        new_user = User(user_name=user_name,
                        password=password,
                        email=email,
                        phone=phone)
        new_user.save()
        return redirect(url_for('homepage'))

@app.route('/sign-in', methods = ['GET', 'POST'])
def sign_in():
    if request.method == "GET":
        return render_template('homepage/sign-in.html')
    elif request.method == "POST":
        form = request.form
        user_name = form['user_name']
        password = form['password']
        user = User.objects(user_name=user_name, password=password)
        if user is None:
            print("not found user name or invalid password")
            return redirect(url_for("wrong"))
        else:
            session['logged_in'] = True
            print("successfully signed in")
            return redirect(url_for("user"))

@app.route('/form', methods = ['GET', 'POST'])
def form():
    if request.method == "GET":
        return render_template('form/setitfree.html')
    elif request.method == "POST":

        form = request.form
        story = form['story']
        price = form['price']
        title = form['title']
        cate = form.getlist('cate')
        list_object = []

        for cate_id in cate:
            cate = Category.objects().with_id(cate_id)
            list_object.append(cate)

        category = list_object

        file1 = request.files.get("file1", None)
        file2 = request.files.get("file2", None)
        file3 = request.files.get("file3", None)

        if file1 == None:
            file_name1 = ""
            print("None")
        else:
            file_name1 = file1.filename
            print("Not none")

        if file2 == None:
            file_name2 = ""
            print("None")
        else:
            print("Not none")
            file_name2 = file2.filename

        if file3 == None:
            file_name3 = ""
            print("None")
        else:
            print("Not none")
            file_name3 = file3.filename

        file_name1= savefile(file1, file_name1)
        file_name2= savefile(file2, file_name2)
        file_name3= savefile(file3, file_name3)

        new_item = Item(story=story,
                        price=price,
                        title=title,
                        image=[file_name1,
                        file_name2, file_name3],
                        category=category)

        new_item.save()

        return redirect(url_for('homepage'))

@app.route('/user')
def user():
    if "logged_in" in session and session["logged_in"] == True:
        return render_template('user/user.html')
    else:
        return redirect(url_for("sign_in"))

@app.route('/wrong')
def wrong():
    return render_template('wrong.html')

@app.route('/user/set-it-free')
def sale():
    return render_template('form/setitfree.html')

if __name__ == '__main__':
  app.run(debug=True)
