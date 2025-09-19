from wtforms import Form,StringField,PasswordField,BooleanField,SubmitField
from wtforms.validators import DataRequired,Length
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField #从flask_cheditor导入

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