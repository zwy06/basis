from django import forms

class MyRegForm(forms.Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密码',widget=forms.PasswordInput)
    password2 = forms.CharField(label='重复密码',widget=forms.PasswordInput)

    def clean_username(self):
        """此方法限定username必须大于等于6个字符"""
        uname = self.cleaned_data['username']
        if len(uname)<6:
            raise forms.ValidationError({"用户名太短"})
        return uname

    def clean(self):
        # 验证两次密码是否一致
        pwd1 = self.cleaned_data['password']
        pwd2 = self.cleaned_data['password2']
        if pwd1 !=pwd2:
            raise forms.ValidationError('两次密码不一样')
        return self.cleaned_data