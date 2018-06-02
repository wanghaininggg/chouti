from django import forms

class SendMsgForm(forms.Form):
    email = forms.EmailField(error_messages={'invalid': '邮箱格式错误'})

class UserInfoForm(forms.Form):
    username = forms.CharField(max_length=32, min_length=6,
                           error_messages={'required': '用户名不能为空', 'max_length':'用户名不能超过32个字符', 'min_length': '用户名不能少于6个字符'})
    email = forms.EmailField(error_messages={'invalid': '邮箱格式错误', 'required':'邮箱不能为空'})
    password = forms.CharField(max_length=64, min_length=8, error_messages={
                          'required': '密码不能为空', 'max_length': '密码不能超过64个字符', 'min_length': '用户名不能少于8个字符'})
    code = forms.CharField(max_length=4, min_length=4, error_messages={'required': '验证码不能为空'})

class LoginForm(forms.Form):
    username = forms.CharField(error_messages={'required': '用户名不能为空'})
    password = forms.CharField(error_messages={'required': '密码不能为空'})
    code = forms.CharField(max_length=4, min_length=4,error_messages={'required': '验证码不能为空'})
