from flask import Flask,render_template, request,redirect,url_for,flash,abort,session,jsonify
import json
import os.path
from werkzeug.utils import secure_filename

app=Flask(__name__)
app.secret_key='dscdsc11dcssd51'

@app.route('/')

def home():
    return render_template('home.html',name='Welcome, Manish...', codes=session.keys())


@app.route('/your_url',methods=['GET','POST'])

def your_url():
    if request.method=='POST':
        urls={}

        if os.path.exists('url_file.json'):
            with open('url_file.json','r') as file:
                urls=json.load(file)

        if request.form['code'] in urls.keys():
            flash('Hey, that shortname has already been taken.')
            return redirect(url_for('home'))
        if 'url' in request.form.keys():
            urls[request.form['code']]={'url':request.form['url']}
        else:
            f = request.files['file']
            full_name=request.form['code']+  secure_filename(f.filename)
            f.save('C:\\Users\\Manish\\Desktop\\Flask\\url_shortner\\static\\user_files\\'+full_name)
            urls[request.form['code']]={'file':full_name}

        with open('url_file.json','w') as file:
            json.dump(urls,file)
            session[request.form['code']]=True

        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))


@app.route('/<string:code>')

def url_redirect(code):
    if os.path.exists('url_file.json'):
        with open('url_file.json','r') as file:
            urls= json.load(file)
            if code in urls.keys():
                if 'url' in urls[code].keys():
                    return redirect(urls[code]['url'])
                if 'file' in urls[code].keys():
                    return redirect(url_for(urls[code]['file']))

    return abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'),404

@app.route('/api')
def session_api():
    return jsonify(list(session.keys()))
