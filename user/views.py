from django.shortcuts import render, get_object_or_404
from blog.models import Author, Content
from blog.md_converter import md_convert
# Create your views here.

def user_page(request, username):
    user = get_object_or_404(Author, username=username)
    blog_list = Content.objects.filter(author=user).order_by('-created_at')

    context = {
        'user': user,
        'latest_blog_list': blog_list,
    }
    print(context)

    return render(request, 'user/user.html', context)
