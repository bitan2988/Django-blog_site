from django import forms
from blog.models import BlogPost

class BlogPostForm(forms.Form):
    title = forms.CharField()
    slug = forms.SlugField()
    content = forms.CharField(widget=forms.Textarea)

 
class BlogPostModelForm(forms.ModelForm):
    #title = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'slug', 'content', 'publish_date']

    def clean_title(self, *args, **kwargs): # self over her is the instance of the form
        # returns a list of names of "interesting" attributes of the instance, 
        # its class, and its parent classes.
        # print(dir(self))
        instance = self.instance
        print(instance)
        title = self.cleaned_data.get('title')
        qs = BlogPost.objects.filter(title__iexact=title)
        if instance is not None:
            # this basically doesnt raise a validation error when we are updating a data
            # as title is set to be unique and when we sill submit the update_form the 
            # title will same as that in the database thus it will raise an error
            # as instance is only passed in the update query
            qs = qs.exclude(pk=instance.pk) # id = pk.id
        if qs.exists():
            raise forms.ValidationError("Title already in use")
        return title 