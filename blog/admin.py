from django.contrib import admin
from django.db import models
from .models import Genre, Content, Author, CV

class GenreAdmin(admin.ModelAdmin):
    model = Genre

class ContentAdmin(admin.ModelAdmin):
    model = Content
    # list_display = ('title', 'genre', 'github_link', 'body_display')

class AuthorAdmin(admin.ModelAdmin):
    model = Author

class CVAdmin(admin.ModelAdmin):
    model = CV

admin.site.register(Genre, GenreAdmin)
admin.site.register(Content, ContentAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(CV, CVAdmin)
