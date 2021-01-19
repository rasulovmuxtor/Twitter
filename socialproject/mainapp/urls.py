from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('new/post/',views.add_post,name = 'add_post'),
    path('like/',views.like,name='like'),
    path('unlike/',views.unlike,name='unlike'),
    path('comment/<int:post_id>',views.new_comment,name='new_comment'),
    path('<user>/',views.user_profile, name='user_profile'),
    path('<user>/<post_id>/',views.post_detail,name='post_detail'),
]