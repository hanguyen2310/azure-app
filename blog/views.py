from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from .models import Content, Author, Genre
from . import md_converter
from django.urls import reverse
from django.utils import timezone
from .forms import BlogForm
import os 
import json
from . import utils

class IndexView(generic.ListView):
    template_name = 'blog/index2.html'
    context_object_name = 'latest_blog_list'

    def get_queryset(self):
        """Return all blog"""
        latest_blog_list = Content.objects.filter(created_at__lte=timezone.now()).order_by('-created_at')[:5]
        for blog in latest_blog_list:
            md_text = utils.read_md_file(blog.body)
            blog.body = md_text[:100]

        return latest_blog_list

def tag_view(request, tag):
    blog_list = Content.objects.filter(tag__contains=tag).order_by('-created_at')

    return render(request, 'blog/index2.html', {'latest_blog_list': blog_list})

def detail(request, pk):
    blog = get_object_or_404(Content, pk=pk)
    md_text = utils.read_md_file(blog.body)
    html_text = md_converter.md_convert(md_text)
    blog.body = html_text
    blog.tag = [tag for tag in blog.tag.split(',') if tag.replace(" ","") != '']
    return render(request, 'blog/detail2.html', {'blog': blog})

def add(request):
    print("here")
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            has_file = False
            has_text = False
            print("valid")
            blog = form.save(commit=False)
            if request.FILES.get('file_upload', False):
                file = request.FILES['file_upload']
                if str(file)[-3:] != '.md':
                    print("[Error] File type not supported")
                    return render(request, 'blog/add.html', {'form': form, 'error_message': 'File type not supported'})
                has_file = True
            else:
                print('No file upload')

            if blog.body != '':
                has_text = True

            if has_file == True:
                blog.body = utils.handle_uploaded_file(file, blog.title)
            else:
                if has_text == True:
                    blog.body = utils.save_md_to_file(blog.body, blog.title)
                else:
                    return render(request, 'blog/add.html', {'form': form, 'error_message': 'Enter something in the body or upload a md file'})

            if request.FILES.get('thumbnail', False):
                thumbnail = request.FILES['thumbnail']
                print("thumbnail uploaded")                
                file_path = utils.save_image(thumbnail, blog.title)
                file_path_to_save = "/".join(file_path.split("/")[2:])
                blog.thumbnail = str(file_path_to_save)
            else:
                print("no thumbnail uploaded. choose a random one.")
                blog.thumbnail = utils.get_random_thumbnail(blog.title)

            blog.updated_at = timezone.now()
            blog.save()
            return HttpResponseRedirect(reverse('blog:index'))
    else:
        form = BlogForm()
    return render(request, 'blog/add.html', {'form': form})

def ajax_preview(request):
    if request.is_ajax() or request.method == 'POST':
        print("ajax here")
        body = request.POST.get('mdtext', "")
        body = md_converter.md_convert(body[1:-1].replace(r'\n', '\n'))
        
        return HttpResponse(json.dumps({'html_output': body}), content_type="application/json", status=200)
    else:
        return HttpResponse("")

def edit(request, pk):
    blog = get_object_or_404(Content, pk=pk)
    md_text = utils.read_md_file(blog.body)
    blog.body = md_text

    return render(request, 'blog/edit.html', {'blog': blog})

def edit_confirm(request, pk):
    blog = get_object_or_404(Content, pk=pk)
    if request.method == 'POST':
        title = request.POST.get("title", "")
        md_text = request.POST.get("markdown_text", "")

        valid = True
        if title != "":
            blog.title = title
        else:
            valid = False
        if md_text != "":
            file_path = blog.body
            utils.update_md_file(file_path, md_text)
        else:
            valid = False

        if valid:
            blog.updated_at = timezone.now()
            blog.save()
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            print("invalid")
            blog.body = md_text
            return render(request, 'blog/edit.html', {'blog': blog, 'error_message': 'Empty title or body'})
    else:
        md_text = utils.read_md_file(blog.body)
        html_text = md_converter.md_convert(md_text)
        blog.body = html_text
        return render(request, 'blog/edit.html', {'blog': blog})