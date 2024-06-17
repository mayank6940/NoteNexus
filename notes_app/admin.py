from django.contrib import admin
from .models import Post, Image

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')
    fields = ('title', 'content', 'image', 'author')
    inlines = [ImageInline]

admin.site.register(Post, PostAdmin)
admin.site.register(Image)