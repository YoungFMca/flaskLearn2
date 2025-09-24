from flask import Flask, flash, render_template,request,make_response
from flask import redirect,url_for,session,send_from_directory
import os

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from forms import LoginForm
from forms import UploadForm,MultiUploadForm,RichTextForm,NewPostForm
from forms import SigninForm,RegisterForm,SigninForm2,RegisterForm2
from flask import request 

from flask import request,session,flash,redirect,url_for
from flask_wtf.csrf import validate_csrf
from wtforms import ValidationError
from flask_ckeditor import CKEditor

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

@app.route('/ckeditor',methods=['GET','POST'])
def ckeditor():
    form=RichTextForm()
    if form.validate_on_submit():
        title=form.title.data
        body=form.body.data
        flash('Your post is published!')
        return render_template('post.html',title=title,body=body)
    return render_template('ckeditor.html',form=form)

@app.route('/two_submits',methods=['GET','POST'])
def two_submits():
    form=NewPostForm()
    if form.validate_on_submit():
        title=form.title.data
        body=form.body.data
        #区分到底点击的是哪个按钮
        if form.save.data:
            flash('You click the save button.')
        elif form.publish.data:
            flash('You click the publish button.')
        return render_template('post.html',title=form.title.data,body=form.body.data)
    return render_template('2submits.html',form=form)

@app.route('/multi-form',methods=['GET','POST'])
def multi_form():
    signin_form=SigninForm()
    register_form=RegisterForm()

    if signin_form.submit1.data and signin_form.validate():
        username=signin_form.username.data
        flash('%s,you just submit the Signin Form.' % username)
        return redirect(url_for('index'))
    if register_form.submit2.data and register_form.validate():
        flash('%s,you just submit the Register Form.' %username)
        return redirect(url_for(index))
    
    return render_template('2form.html',signin_form=signin_form,register_form=register_form)
#
@app.route('/multi-form-multi-view')
def multi_form_multi_view():
    signin_form=SigninForm2()
    register_form=RegisterForm2()
    return render_template('2form2view.html',signin_form=signin_form,
                           register_form=register_form)

@app.route('/handle-signin',methods=['POST'])
def handle_signin():
    signin_form=SigninForm2()
    register_form=RegisterForm2()

    if signin_form.validate_on_submit():
        username=signin_form.username.data
        flash('%s,you ust submit the signin Form.' %username)
        return redirect(url_for('index'))
    return render_template('2form2view.html',signin_form=signin_form,register_form=register_form)

@app.route('/handle-register',methods=['POST'])
def handle_register():
    signin_form=SigninForm2()
    register_form=RegisterForm2()

    if register_form.validate_on_submit():
        username=register_form.username.data
        flash('%s,you just submit the Register Form.' %username)
        return redirect(url_for('index'))
    return render_template('2form2view.html',signin_form=signin_form,register_form=register_form)

# def flash_errors(form):
#     for field,errors in form.errors.items():
#         for error in errors:
#             flash('Error in the %s field - %s' %(getattr(form,field).label.text,error))

if __name__ == '__main__':
    app.jinja_env.auto_reload=True
    app.config['TEMPLATES_AUTO_RELOAD']=True
    app.secret_key=os.getenv('SECRET_KEY','secret string')
    app.config['ALLOWED_EXTENSIONS']=['png','jpg','jpeg','gif']
    app.config['UPLOAD_PATH']=os.path.join(app.root_path,'uploads')#路径 uploads文件夹
    # Flask-CKEditor config
    app.config['CKEDITOR_SERVE_LOCAL'] = True
    app.config['CKEDITOR_FILE_UPLOADER'] = 'ckeditor'
    app.secret_key=os.getenv('SECRET_KEY','secret string')#用来获取环境变量中的密钥 第二个参数是默认值
    ckeditor = CKEditor(app)

    app.run(host='0.0.0.0', port=5000, debug=True)

# @app.before_first_request
# def befor_first_request():
#     print("Starting the Flask app...")
#     print(app.url_map)
