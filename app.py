from flask import Flask, flash, render_template,request,make_response
from flask import redirect,url_for,session,send_from_directory
import os

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from forms import LoginForm
from forms import UploadForm,MultiUploadForm
from flask import request 

from flask import request,session,flash,redirect,url_for
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError

#from werkzeug import secure_filename
import uuid as uid
#https://github.com/greyli/helloflask/tree/main/demos/form

app=Flask(__name__)

#上传文件的时候给文件随机的文件名
def random_filename(filename):
    ext=os.path.splitext(filename)[1]
    new_filename=uid.uuid4().hex+ext
    return new_filename

#concede if this can be used
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']



@app.route('/hello')
def hello():
    name=request.args.get('name') or request.cookies.get('name')
    return '<h1>Hello,%s!<h1>' %name

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set/<name>')
def set_cookie(name):
    response=make_response(redirect(url_for('hello'))) #
    response.set_cookie('name',name)
    return response

@app.route('/basic',methods=['GET','POST'])
def basic():
    form=LoginForm()
    #if request.method=='POST' and form.validate:
    if form.validate_on_submit():#与上面的等价
        username=form.username.data
        flash('Welcome home,%s!' %username)
        return redirect(url_for('index'))
    return render_template('basic.html',form=form) 


#@app.route('/uploads/<path:filename>')
#def get_file(filename):
#    print("filename is here:"+filename)
#    return send_from_directory(app.config['UPLOAD_PATH'],filename)
@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/uploaded-images')
def show_images():
    return render_template('uploaded.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = random_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('Upload success.')
        session['filenames'] = [filename]
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)



#20250911 多文件上传
@app.route('/multi-upload',methods=['GET','POST'])
def multi_upload():
    form=MultiUploadForm()

    if request.method=='POST':
        filenames=[]
        #验证CSRF令牌
        try:
            validate_csrf(form.csrf_token.data) 
        except ValidationError:
            flash('CSRF token error.')
            return redirect(url_for('multi_upload'))
        
        photos=request.files.getlist('photo')
        #检查文件是否存在
        if not photos[0].filename:
            flash('No selected file.')
            return redirect(url_for('multi_upload'))
        for f in photos:
            #检查文件类型
            if f and allowed_file(f.filename): #用来确保文件对象存在
                filename=random_filename(f.filename)
                f.save(os.path.join(
                    app.config['UPLOAD_PATH'],filename
                    ))
                filenames.append(filename)
            else:
                flash('Invalid file type.')
                return redirect(url_for('multi_upload'))
        flash('Upload success.')
        session['filenames']=filenames
        return redirect(url_for('show_images'))
    return render_template('upload.html',form=form)



if __name__ == '__main__':
    app.jinja_env.auto_reload=True
    app.config['TEMPLATES_AUTO_RELOAD']=True
    app.secret_key=os.getenv('SECRET_KEY','secret string')
    app.config['ALLOWED_EXTENSIONS']=['png','jpg','jpeg','gif']
    app.config['UPLOAD_PATH']=os.path.join(app.root_path,'uploads')#路径 uploads文件夹
    app.secret_key=os.getenv('SECRET_KEY','secret string')#用来获取环境变量中的密钥 第二个参数是默认值
    app.run(host='0.0.0.0', port=5000, debug=True)

@app.before_first_request
def befor_first_request():
    print("Starting the Flask app...")
    print(app.url_map)
