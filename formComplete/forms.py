from wtforms import Form,StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length,Email
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField #从flask_cheditor导入


class SigninForm2(FlaskForm):
    username=StringField('用户名',validators=[DataRequired(),Length(1,20)])
    password=PasswordField('密码',validators=[DataRequired(),Length(8,128)])
    remember=BooleanField('记住我')
    submit=SubmitField('注册')
#
class RegisterForm2(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(1,20)])
    email=StringField('Email',validators=[DataRequired(),Email(),Length(1,253)])
    password=PasswordField('Password',validators=[DataRequired(),Length(1,254)])
    submit=SubmitField('Register')

class SigninForm(FlaskForm):
    username=StringField('用户名',validators=[DataRequired(),Length(1,20)])
    password=PasswordField('密码',validators=[DataRequired(),Length(8,128)])
    remember=BooleanField('记住我')
    submit1=SubmitField('注册')
#
class RegisterForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired(),Length(1,20)])
    email=StringField('Email',validators=[DataRequired(),Email(),Length(1,253)])
    password=PasswordField('Password',validators=[DataRequired(),Length(1,254)])
    submit2=SubmitField('Register')

class NewPostForm(FlaskForm):
    title=StringField('标题',validators=[DataRequired(),Length(1,50)])
    body=CKEditorField('正文',validators=[DataRequired()])
    save=SubmitField('Save') #提交按钮
    publish=SubmitField('Publish') #发布按钮

class RichTextForm(FlaskForm):#富文本编辑器窗口
    title=StringField('Title',validators=[DataRequired(),Length(1,50)])
    body=CKEditorField('Body',validators=[DataRequired()])
    submit=SubmitField('Publish')

class LoginForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    password=PasswordField('Password',validators=[DataRequired(),Length(8,128)])
    remember=BooleanField('Remember me')
    submit=SubmitField('Log in')

from flask_wtf.file import FileField,FileRequired,FileAllowed,MultipleFileField
class UploadForm(FlaskForm):
    photo=FileField('Upload Image',validators=[FileRequired(),
                                               FileAllowed(['jpg','jpeg','png','gif'])])
    submit=SubmitField()

class MultiUploadForm(FlaskForm):
    photo=MultipleFileField('Upload Image',validators={DataRequired()})
    submit=SubmitField()