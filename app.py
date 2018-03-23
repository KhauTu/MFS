from flask import *
from models.service import Item
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

@app.route('/form', methods = ['GET', 'POST'])
def form():
    if request.method == "GET":
        return render_template('form.html')
    elif request.method == "POST":

        form = request.form
        name = form['name']
        phone = form['phone']
        address = form['address']
        story = form['story']
        price = form['price']
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

        new_item = Item(name=name,
                            phone=phone,
                            address=address,
                            story=story,
                            price=price,
                            image=[file_name1,
                            file_name2, file_name3]
                            )

        new_item.save()

        return redirect(url_for('homepage'))

@app.route('/login')
def login():
        return render_template('login.php')

if __name__ == '__main__':
  app.run(debug=True)
