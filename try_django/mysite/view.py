# a function that can render out someting MVT(Model View Template)

from django.http import HttpResponse
from django.shortcuts import render
from .forms import ContactForm
from blog.models import BlogPost


def homePage(request):
    title = "Hello there..."
    qs = BlogPost.objects.all()[:5]
    context = {"title":"Welcome to my blob website", 'blog_list':qs}
    # if request.user.is_authenticated:
    #     context = {"title":title, "my_list":[1, 2, 3, 4]}
    # doc = f"<h1>{title}</h1>"
    # django_rendered_doc = "<h1>{{title}}</h1>".format(title=title)
    return render(request, "home.html", context)


def aboutPage(request):
    return render(request, "about.html", {"title":"About Us"})
    # return render(request, "hello_world.html", {"title":"About Us"}) # rendering context inside a django template
    # return HttpResponse("<h1>About Us</h1>")


def contactPage(request):
    form = ContactForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        form = ContactForm()  # reset the form after data is submitted
    context = {
        "title":"Contact Us",
        "form":form
    }
    return render(request, "form.html", context)
    