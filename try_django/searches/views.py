from django.shortcuts import render
from .models import SearchQuery
from blog.models import BlogPost

def search_view(request):
    q = request.GET.get('q', None)
    user = None
    if request.user.is_authenticated:
        user = request.user
    context = {"query":q}
    if q is not None:
        SearchQuery.objects.create(user=user, query=q)
        blog_list = BlogPost.objects.search(query=q)
        context['blog_list'] = blog_list
    return render(request, 'searches/view.html', context)  