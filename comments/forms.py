from captcha.fields import CaptchaField
from django import forms

from comments.models import Comment


class CommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ['username', 'email', 'homepage', 'text',  'captcha']

    def clean_text(self):
        text = self.cleaned_data.get('text')
        allowed_tags = ['b', 'i']
        for tag in allowed_tags:
            text = text.replace(f"<{tag}>", "").replace(f"</{tag}>", "")
        if "<" in text or ">" in text:
            raise forms.ValidationError("HTML tags are not allowed except for <b> and <i>.")
        return text