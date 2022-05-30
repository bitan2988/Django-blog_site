# Django Form
# Django automatically does form validation
# like you cant leave a block empty or cant put invalid email-id
import email
from django import forms

class ContactForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)

    # form validation
    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        if email.endswith('.edu'):
            raise forms.ValidationError("Not a valid emial")
        return email