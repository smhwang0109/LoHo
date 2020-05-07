from django import forms
from .models import Article, Comment
from django.core.validators import MaxValueValidator, MinValueValidator, MinLengthValidator
from bootstrap_datepicker_plus import DateTimePickerInput
from ckeditor_uploader.widgets import CKEditorUploadingWidget

def unit_100(value):
    if value%100:
        raise forms.ValidationError('100원 단위로 입력해주세요.')


class UploadForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('author', 'created_at', 'updated_at', 'man_participations', 'woman_participations')
        widgets = {
            'title' : forms.TextInput(
                attrs={'class':'form-control', 'style':'width:100%', 'placeholder': '제목을 입력하세요.'}
            ),
            'event_date' : DateTimePickerInput(
                options={
                "showClose": True,
                "showClear": True,
                "showTodayButton": True,
                }
            ) 
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('author', 'article', 'created_at', 'updated_at')
        widgets = {
            'rank' : forms.NumberInput(
                attrs={
                    'min':0,
                    'max':5,
                    'class':'d-line w-25'
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'rows':2
                }
            )
        }
