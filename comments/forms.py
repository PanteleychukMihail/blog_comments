from django import forms
from django.contrib.auth.forms import AuthenticationForm

from captcha.fields import CaptchaField

from comments.models import Comment


class LoginUserForm(AuthenticationForm):
    """Authentication form for users.
       """
    username = forms.CharField(label='User', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.TextInput(attrs={'class': 'form-input'}))


class CommentForm(forms.ModelForm):
    """Form for adding comments with captcha validation.
        """
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ['email', 'homepage', 'text',  'captcha']

    def clean_text(self) -> str:
        """Clean and validate the comment text.
        """
        text: str = self.cleaned_data.get('text')
        allowed_tags: list = ['b', 'i']

        for tag in allowed_tags:
            text = text.replace(f"<{tag}>", "").replace(f"</{tag}>", "")

        if "<" in text or ">" in text:
            raise forms.ValidationError("HTML tags are not allowed except for <b> and <i>.")

        return text