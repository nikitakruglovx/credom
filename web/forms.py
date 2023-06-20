from django import forms
from matplotlib import widgets
from .models import CloudFiles, Items, Users, Folder
from django.forms import ModelForm, TextInput, FileInput, Textarea, Select
from captcha.fields import CaptchaField, CaptchaTextInput

class CloudFilesForm(forms.ModelForm):
    class Meta:
        model = CloudFiles
        fields = ['file', 'folder']

        widgets = {
            'file': FileInput(attrs={
                'type': 'file',
                'id': 'upload-file'
            }),
            'folder': Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, user, *args, **kwargs):
        super(CloudFilesForm, self).__init__(*args, **kwargs)
        self.fields['folder'].queryset = Folder.objects.filter(author_folder=user)
        

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['folder', 'password_folder']

        widgets = {
            'folder': TextInput(attrs={
                'class': 'form-control',
                'type': 'text',
                'placeholder': 'Название нового раздела',
                'style': 'height: 40px;'
            }),
            'password_folder': TextInput(attrs={
                'class': 'form-control',
                'type': 'password',
                'placeholder': 'Пароль который будет защищать этот раздел',
                'style': 'height: 40px;'
            })
        }



class UsersForm(ModelForm):
    class Meta:
        model = Users
        fields = ['who_member', 'avatar_profile', 'background_profile']

        widgets = {
            'avatar_profile': FileInput(attrs={
                'class': 'custom-file-input',
                'type': 'file'
            }),
            'who_member': TextInput(attrs={
                'class': 'form-control input-default',
                'placeholder': 'Специальность'
            }),
            'background_profile': FileInput(attrs={
                'class': 'custom-file-input',
                'type': 'file'
            }),
        }

class ItemForm(ModelForm):
    class Meta:
        model = Items
        fields = ['photo_item', 'name_item', 'text_item', 'price_item' , 'choice_group', 'two_photo_item', 'tree_photo_item', 'four_photo_item', 'archive_file', 'file_link']

        widgets = {
            'photo_item': FileInput(attrs={
                'class': 'custom-file-input',
                'type': 'file'
            }),
            'name_item': TextInput(attrs={
                'class': 'form-control input-default',
                'placeholder': 'Название'
            }),
            'text_item': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Полное описание',
                'id': 'comment',
                'rows': '4'
            }),
            'price_item': TextInput(attrs={
                'class': 'form-control input-default',
                'maxlength': '10',
                'value': '0.00000000',
                'placeholder': 'Цена за товар в ETH'
            }),
            'choice_group': Select(attrs={
                'class': 'form-select'
            }),
            'two_photo_item': FileInput(attrs={
                'class': 'custom-file-input',
                'type': 'file'
            }),
            'tree_photo_item': FileInput(attrs={
                'class': 'custom-file-input',
                'type': 'file'
            }),
            'four_photo_item': FileInput(attrs={
                'class': 'custom-file-input',
                'type': 'file'
            }),
            'archive_file': FileInput(attrs={
                'class': 'custom-file-input',
                'type': 'file'
            }),
            'file_link': TextInput(attrs={
                'class': 'form-control input-default',
                'value': 'Ссылка на товар',
                'placeholder': 'Ссылка на товар'

            }),
        }

class FeedbackForm(forms.Form):
    contact = forms.CharField(min_length=5, max_length=50)
    messagess = forms.CharField(min_length=5)
    captcha = CaptchaField()
