from flask import Flask ,render_template,flash
from flask_wtf import FlaskForm
from wtforms import StringField,RadioField,PasswordField
from wtforms.validators import DataRequired,InputRequired,EqualTo

from datetime import datetime
import pymongo
from pymongo import MongoClient

app=Flask(__name__)
app.config['SECRET_KEY']='secret-key'
#app.config['MONGO_URI']="mongodb+srv://gsrarpramod:marvel@cluster0.ygd2igb.mongodb.net/?retryWrites=true&w=majority"


#setup mongodb
#mongodb_client=PyMongo(app)
#db=mongodb_client.db

myclient=MongoClient("mongodb+srv://example:Password@cluster0.cipfpam.mongodb.net/?retryWrites=true&w=majority")
mydb=myclient["mydatabase"]

collection=mydb["sigin"]




class MyForm(FlaskForm):
    name = StringField('name :', validators=[DataRequired()])
    gender=RadioField('Gender :',choices=[('Male'),('Female')],validators=[DataRequired()])
    password = PasswordField('New Password :', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password :')
    
#encrytion of data
def encry(a):
    key=3
    s=""
    for i in range(len(a)):
       da=ord(a[i])+key
       s=s+chr(da)
    return s 

@app.route('/',methods=['GET','POST'])
def Sign_In():
    form=MyForm()
    if form.validate_on_submit():
        fo_name=form.name.data
        fo_gender=form.gender.data
        fo_pas=encry(form.password.data)
        print(fo_name,fo_gender,fo_pas)
        collection.insert_one({
            "name":fo_name,
            "gender":fo_gender,
            "password":fo_pas,
            "date":datetime.utcnow()
        })
        flash("success","success")
        return render_template('a7.html',name=form.name.data)

    return render_template('a6.html',form=form)

if __name__=='__main__':
    app.run(debug=True)
