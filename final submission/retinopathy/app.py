import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from keras.models import load_model
from keras.preprocessing import image
from keras.applications.inception_v3 import preprocess_input
from keras_preprocessing.image import load_img, img_to_array
import requests
from flask import Flask, request, render_template, redirect, url_for
from cloudant.client import Cloudant

model = load_model(r'uploads/updated-Xception-diabetic-retinopathy.h5')

app = Flask(__name__, template_folder='templates')


#Authenticate using an IBM API key
client = Cloudant.iam('82241234-0f27-4001-9768-39779dda2122-bluemix','yyEb_ODgLWlsuaoiyYQiOMjaaFGI1CKGYYYL8M95OEXY',connect = True)

#create a database using an initialized client
my_database = client.create_database('my_database')


# default home page or route
@app.route('/')
def index():
    return render_template('index.html', pred="Login", vis ="visible")

@ app.route('/index.html')
def home():
    login=False
    if 'user' in session:
        login=True
    return render_template("index.html", pred="Login", vis ="visible",login=login)

#registration page
@ app.route('/register.html',methods=["GET","POST"])
def register():
    if request.method == "POST":
        name =  request.form.get("name")
        mail = request.form.get("emailid")
        pswd = request.form.get("pass")
        pswd = request.form.get("pass")
        data = {
            'name': name,
            'mail': mail,
            'psw': pswd,
            'psw': pswd
        }
        print(data)
        query = {'mail': {'$eq': data['mail']}}
        docs = my_database.get_query_result(query)
        print(docs)
        print(len(docs.all()))
        if (len(docs.all()) == 0):
            url = my_database.create_document(data)
            return render_template("register.html", pred=" Registration Successful , please login using your details ")
        else:
            return render_template('register.html', pred=" You are already a member , please login using your details ")
    else:
        return render_template('register.html')   


#login page
@ app.route('/login.html', methods=['GET','POST'])
def login():
    if request.method == "GET":
        user = request.args.get('mail')
        passw = request.args.get('pass')
        print(user, passw)
        query = {'mail': {'$eq': user}}
        docs = my_database.get_query_result(query)
        print(docs)
        print(len(docs.all()))
        if (len(docs.all()) == 0):
            return render_template('login.html', predict="")
        else:
            if ((user == docs[0][0]['mail'] and passw == docs[0][0]['psw'])):
                session['user'] = user
                flash("Logged in as " + str(user))
                return render_template('index.html', predict="Logged in as "+str(user), vis ="hidden", vis2="visible")
            else:
                return render_template('login.html', predict="The password is wrong.")
    else:
        return render_template('login.html')

# logout page
@ app.route('/logout')
def logout():
    session.pop('user',None)
    return render_template('logout.html')

# prediction page
@app.route('/predict', methods = ["GET","POST"])
def res():
    if request.method=="POST":
        f = request.files['file']
        basepath = os.path.dirname(__file__)#getting  the currnet path i.e where app.py is present
        #print("current path", basepath)
        filepath = os.path.join(basepath, 'uploads', f.filename)#from anywhere in the system we can give imagebut we want that
        print("upload folder is", filepath)
        f.save(filepath)

        img = load_img(filepath, target_size = (299, 299))
        x = img_to_array(img)#img to array
        x = np.expand_dims(x, axis = 0)#used for adding one more simension
        #print(x)
        img_data = preprocess_input(x)
        prediction = np.argmax(model.predict(img_data), axis = 1)

        #prediction = model.predict(x)#instead of predict_classes(x) we can use predict(x) ----> predict_classes(x) gave error
        #print("prediction is ", prediction)
        index = ['No Diabetic REtinopathy', 'mild DR', 'Moderate DR', 'Severe DR', 'Proliferative DR']
        #result = str(index[output[0]])
        result = str(index[prediction[0]])
        print("result = " , result)

        
        return render_template("predictor.html" , prediction = result)
    else:
        return render_template('predictor.html')

if __name__ == "__main__":
    app.run(debug = False)