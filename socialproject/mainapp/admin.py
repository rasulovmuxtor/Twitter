from django.contrib import admin

from .models import Post, Like, Repost, Comment, UserFollowing

admin.site.register([Post, Like, Repost, Comment, UserFollowing])



# @admin.register(Image)
# class ImageAdmin(admin.ModelAdmin):
# list_display = ['title', 'slug', 'image', 'created']
# list_filter = ['created']