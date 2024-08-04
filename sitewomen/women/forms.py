from django import forms
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

from .models import Category, Husband
from django.core.validators import MinLengthValidator, MaxLengthValidator


@deconstructible
class RussianValidator:
    ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабегдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '
    code = 'russian'

    def __init__(self, message=None):
        self.message = message if message else 'Должны присутствовать символы кирилицы, числа от 0 до 9 дефис и пробел'

    def __call__(self, value, *args, **kwargs):
        if not (set(value) <= set(self.ALLOWED_CHARS)):
            raise ValidationError(self.message, code=self.code)


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, min_length=5,
                            label='Заголовок Статьи',
                            widget=forms.TextInput(attrs={'class': 'form-input'}),
                            validators=[
                                RussianValidator()
                            ],
                            error_messages={
                                'min_length': 'Слишком короткий заголовок',
                                'required': 'Без заголовка никак'
                            })
    slug = forms.SlugField(max_length=255, label='URL',
                           validators=[
                               MinLengthValidator(5, message='Минимум 5 символов'),
                               MaxLengthValidator(100, message='Максимум 100 символов')
                           ])
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 100, 'rows': 5}), required=False, label='Содержимое')
    is_publisher = forms.BooleanField(required=False, initial=True, label='Статус')
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='Выберите категорию', label='Категории')
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), required=False, empty_label='Не замужем', label='Муж')

    def clean_title(self):
        title = self.cleaned_data['title']
        ALLOWED_CHARS = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабегдеёжзийклмнопрстуфхцчшщьыъэюя0123456789- '

        if not (set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError('Должны присутствовать символы кирилицы, числа от 0 до 9 дефис и пробел')
