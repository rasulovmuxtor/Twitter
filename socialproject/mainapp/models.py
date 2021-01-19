from django.db import models
from django.db.models import Q
from django.conf import settings
from django.urls import reverse
from itertools import chain
from operator import attrgetter




class Post(models.Model):
    poster = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts',on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)
     
    class Meta:
        ordering=['-created']
    def like_count(self):
        return self.likes.count()
    def comment_count(self):
        return self.comments.count()
    def repost_count(self):
        return self.reposts.count()
    def poster_url(self):
        return reverse('user_profile', args=[self.poster.username])
    def post_url(self):
        return reverse('post_detail',args=[self.poster.username, self.id])
        

class Comment(Post):
    post = models.ForeignKey(Post, related_name='comments',on_delete=models.CASCADE)
    
class Like(models.Model):
    liker = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='likes',on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='likes',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'liker')

class Repost(models.Model):
    repost_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reposts',on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='reposts',on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


#Relationship
class UserFollowing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following',on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followed_by',on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'following')



def by_user(user):
    followings = UserFollowing.objects.filter(user=user).values_list('following',flat=True)
    
    comment = Comment.objects.filter(Q(poster__in=followings) | Q(poster=user))
    post = Post.objects.filter(Q(poster__in=followings) | Q(poster=user)).exclude(id__in = comment.values_list('id',flat=True))
    repost = Repost.objects.filter(Q(repost_by__in=followings) | Q(repost_by=user))
    like = Like.objects.filter(Q(liker__in=followings) | Q(liker=user))
  
    # all_posts = post | repost | like | comment
    all_posts = sorted(
        chain(post,repost,like,comment),
        key=attrgetter('created'),
        reverse=True
    )
    return all_posts