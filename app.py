from flask import *
from models.service import Item, Category, User
import mlab
import os
from werkzeug.utils import secure_filename
# from flask_disqus import Disqus

mlab.connect()

app = Flask(__name__)
# disq = Disqus(app)

app.config['SECRET_KEY'] = "Memoryforsales123"

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

@app.route('/', methods=['GET', "POST"])
def homepage():
    all_items = Item.objects()
    # return render_template('homepage.html', all_items = all_items)
# @app.route('/sign-up', methods = ['GET','POST'])
# def sign_up():
    if request.method == "GET":
        # return render_template('homepage/sign-up.html')
        user_name = session.get('user_name', None)
        if user_name != None:
            user = User.objects(user_name = user_name)[0]
        return render_template('homepage.html', all_items = all_items, message = '', user_name = user_name, user = user)
    elif request.method == "POST":
        form = request.form

        user_name = form.get('user_name', None)
        password = form.get('password', None)
        email = form.get('email', None)
        phone = form.get('phone', None)

        user = form.get('user', None)
        pas = form.get('pass', None)

        if email == None:

            user = User.objects(user_name=user, password=pas)
            if len(user) == 0:
                message = "not found user name or invalid password"
                show_example_modal=True
                return render_template('homepage.html', all_items = all_items, message = message)
            else:
                session['logged_in'] = True
                session['user_name'] = user[0].user_name
                print("successfully signed in")
                return redirect(url_for("user", user_name = user[0].user_name))
        else:

            new_user = User(user_name=user_name,
                            password=password,
                            email=email,
                            phone=phone)
            new_user.save()
            return redirect(url_for('homepage'))

# @app.route('/sign-in', methods = ['GET', 'POST'])
# def sign_in():
    # if request.method == "GET":
    #     return render_template('homepage/sign-in.html')

@app.route('/user/<user_name>/set-it-free', methods = ['GET', 'POST'])
def form(user_name):
    if request.method == "GET":
        return render_template('form/setitfree.html', user_name=user_name)
    elif request.method == "POST":

        form = request.form
        name = form['name']
        print(name)
        phone = form['phone']
        address = form['address']
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

        new_item = Item(name = name,
                        phone = phone,
                        address = address,
                        story=story,
                        price=price,
                        title=title,
                        image=[file_name1,
                        file_name2, file_name3],
                        category=category)

        new_item.save()

        return redirect(url_for('homepage'))

@app.route('/user/<user_name>')
def user(user_name):
    user = User.objects(user_name = user_name)
    products = Item.objects(name = user_name)
    print(products)
    if "logged_in" in session and session["logged_in"] == True:
        return render_template('user/user.html', user = user[0], products = products)
    else:
        return redirect(url_for("homepage"))

@app.route('/wrong')
def wrong():
    return render_template('wrong.html')



if __name__ == '__main__':
  app.run(debug=True)
