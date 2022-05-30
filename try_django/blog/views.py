from re import template
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
from .models import BlogPost
from .forms import BlogPostForm, BlogPostModelForm

# def blog_post_detail_page(request, slug):
#     # obj = BlogPost.objects.get(id=post_id) 
#     # obj = get_object_or_404(BlogPost, slug=slug) # does the try: except: block
#     querySet = BlogPost.objects.filter(slug=slug)  # returns a list of queries that match the condition
#     if querySet.count() == 0:
#         raise Http404
    
#     obj = querySet.first()  # querySet[0]
    
#     template_name = "blog_post_detail.html"
#     context = {"object":obj}  # we will unpack obj inside our template
#     return render(request, template_name, context)


# CRUD 
def blog_post_list_view(request):
    # list out object / search for several objects
    qs = BlogPost.objects.all().published()  # returns a query_set aka list of python objects
    # qs = BlogPost.objects.filter()  # to filter those results
    if request.user.is_authenticated:
        my_qs = BlogPost.objects.filter(user=request.user)
        qs = (qs | my_qs).distinct()
    template_name = 'blog/list.html'
    context = {'object_list':qs}
    return render(request, template_name, context)


# log-in for create
# @login_required  # (login_url='/login')  implies for this part we will need authentication
@staff_member_required
def blog_post_create_view(request):
    # create objects using a form
    # form = BlogPostForm(request.POST or None)
    # if not request.user.is_authenticated:
    #     return render(request, "not-a-user.html", {})
    form = BlogPostModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        # form.save() -> can only use this if its a ModelForm
        obj = form.save(commit=False)
        # obj.title = form.cleaned_data.get("title") + "string_append"
        obj.user = request.user  # set user as the user who is currently logged in
        obj.save()
        # print(form.cleaned_data)
        # we can grab data of a single fiels too 
        # title = form.cleaned_data['title']
        # ** unpack/ turn the key-value pair into arguments
        # obj = BlogPost.objects.create(**form.cleaned_data)
        form = BlogPostModelForm()
    template_name = 'form.html'
    context = {'form':form} # will be an object
    return render(request, template_name, context)


def blog_post_detail_view(request, slug):
    # retrieve detail view of 1 object
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = "blog/detail.html"
    context = {"object":obj}  # we will unpack obj inside our template
    return render(request, template_name, context)
    

@staff_member_required
def blog_post_update_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    form = BlogPostModelForm(request.POST or None, instance=obj) # instance allows us to pass and object
    if form.is_valid():
        form.save()
    template_name = "form.html"
    context = {'form':form, 'title':f'Update {obj.title}'}  
    return render(request, template_name, context)


@staff_member_required
def blog_post_delete_view(request, slug):
    obj = get_object_or_404(BlogPost, slug=slug)
    template_name = "blog/delete.html"
    if request.method=="POST":
        obj.delete()
        return redirect("/blog")   # redirect after the method has happened
    context = {"object":obj} 
    return render(request, template_name, context)
    
 