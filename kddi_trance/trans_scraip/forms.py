from django import forms

class UploadFileForm(forms.Form):
    # formのname 属性が 'file' になる
    file = forms.FileField(required=True, label='')
