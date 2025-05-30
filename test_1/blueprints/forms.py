import wtforms
from wtforms.validators import Email,Length,EqualTo
from models import UserModel
from exts import db
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    username = wtforms.StringField(validators=[Length(min=3,max=20,message="用户名格式错误")])
    password = wtforms.StringField(validators=[Length(min=6,max=20,message="密码格式错误")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password",message="两次密码不一致")])
    #自定义验证：
    # 1邮箱是否被注册；
    def validate_email(self,field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user :
            raise wtforms.ValidationError(message="该邮箱已经被注册")