from bson.objectid import ObjectId
from flask import Flask,render_template,request,redirect,url_for,flash,send_from_directory,jsonify,session,g
from werkzeug.utils import secure_filename
import os
from bson.json_util import dumps
from flask_pymongo import PyMongo
from transcription.speech_to_text import recognize
from werkzeug.security import generate_password_hash,check_password_hash
import datetime

ALLOWED_EXTENSIONS = {'wav'}

app = Flask(__name__)
app.secret_key = 'super-secret-key'
app.config['SESSION_TYPE'] = 'filesystem'
# app.config["MONGO_URI"] = "mongodb+srv://Anurag:322KUEf7mJ7DPBKB@anuragscluster.j2ski.mongodb.net/meetify?retryWrites=true&w=majority"
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/meetify"
mongo = PyMongo(app)

@app.before_request
def before_request():
    g.email = None
    if 'user_mail' in session:
        # user = [x for x in users if x.id == session['user_id']][0]
        g.email = session['user_mail']
        g.username = session['user_name']
        g.userID = mongo.db.users.find_one({'email' : g.email}, {'_id': 1})


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    if g.email:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register')
def register():
    if g.email:
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    g.email = None
    session.clear()
    return redirect('login')

@app.route('/loginRequest',methods=['GET','POST'])
def loginRequest():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        return False
    user = mongo.db.users.find_one({'email':email})
    if user:
        if check_password_hash(user['password'],password):
            session.pop('user_mail', None)
            session['user_mail'] = user['email']
            session['user_name'] = user['name']
            return jsonify(login=True),200
        else:
            return jsonify(invalid=True), 403
    else:
        return jsonify(notFound=True), 401

@app.route('/registerRequest',methods=['GET','POST'])
def registerRequest():
    if request.method == 'POST':
        json = request.json
        email = json['email']
        pwd = json['password']
        name = json['name']
        user = mongo.db.users.find_one({'email':email})
        if user:
            return jsonify(error='Email Already Exists'), 409
        else:
            try:
                _hashed_password = generate_password_hash(pwd)
                print("helo \n")
                _id = mongo.db.users.insert({'name':name,'email':email,'password':_hashed_password,'meets':[]})
                session.clear()
                session['user_mail'] = email
                session['user_name'] = name
                return jsonify(register=True), 200
            except:
                return jsonify(register=False), 500

@app.route('/profile')
def profile():
    if not g.email:
        return redirect(url_for('login'))
    return render_template('profile.html')


@app.route('/password_update', methods=['POST'])
def password_update():
    if not g.email:
        return redirect(url_for('login'))
    email = request.json['email']
    oldpass = request.json['oldpass']
    newpass =request.json['newpass'] 
    user = mongo.db.users.find_one({'email':email})
    if user:
        if check_password_hash(user['password'],oldpass):
            _hashed_password = generate_password_hash(newpass)
            mongo.db.users.update_one({'email':email},{'$set':{'password':_hashed_password}})
            return jsonify(success=True), 200
        else:
            return jsonify(incorrect=True), 401
    else:
        return jsonify(error=True), 404


# schedule
@app.route('/schedule')
def schedule():
    if not g.email:
        return redirect(url_for('login'))
    d = mongo.db.users.aggregate([
        {"$match": {"_id": {'$ne': g.userID['_id']}}},
        {'$project': {'_id': {'$toString': "$_id"},'name':1}}
    ])
    return render_template('schedule.html',users = dumps(d))

@app.route('/scheduleRequest',methods=['GET','POST'])
def scheduleRequest():
    if not g.email:
        return redirect(url_for('login'))
    title = request.json['title']
    description = request.json['desc']
    date = request.json['date'] 
    meetID = request.json['link'] 
    addedPeople = request.json['addedPeople'] 
    addedPeople.append({'owner':True,'_id': str(g.userID['_id']), 'name': g.username})
    meet = mongo.db.meetings.find_one({'meetID':meetID})
    if not meet:
        d = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M")
        _id = mongo.db.meetings.insert_one({"title":title,'description':description,'status':'scheduled','date':d,'meetID':meetID,'ownerID':str(g.userID['_id']),'people':addedPeople})
        return jsonify(success=True), 200
    else:
        return jsonify(error=True), 403


@app.route('/mymeets')
def myMeets():
    if not g.email:
        return redirect(url_for('login'))
    res = mongo.db.meetings.find({"people._id" : str(g.userID['_id']),"ownerID" :str(g.userID['_id'])})
    invited =  mongo.db.meetings.find({'people._id': str(g.userID['_id']),"ownerID":{ "$ne": str(g.userID['_id'])}})
    return render_template('myMeets.html',ownmeets = dumps(res),invited=dumps(invited))


@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if not g.email:
        return redirect(url_for('login'))
    if request.method == 'POST':
        print("REQUEST : \n")
        print(request.form.to_dict)
        return redirect('editor')
    return render_template('dashboard.html')




@app.route('/meetDetails/<key>',methods=['GET','POST'])
def meetDetails(key):
    if not g.email:
        return redirect(url_for('login'))
    if request.method == 'POST':
        print("REQUEST : \n")
        print(request.form.to_dict)
        return redirect('editor')
    return render_template('meetDetails.html',key=key)




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/audio-input',methods=['GET','POST'])
def audiototext():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if allowed_file(file.filename):
            if file:
                filename = secure_filename(file.filename)   
                file.save(os.path.join("uploads",filename))
                text = recognize(filename)
                session['text'] = text
                return redirect(url_for('uploaded_file'))
        else:
            flash('Unsupported FileType')
            return redirect(request.url)
    return render_template('audioinput.html')

@app.route('/uploads')
def uploaded_file():
    return render_template('output.html',text = session['text'])


@app.route('/editor')
def live():
    return render_template('editor.html')
