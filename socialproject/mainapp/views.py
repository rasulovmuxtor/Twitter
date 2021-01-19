from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.http import JsonResponse,HttpResponse
from .forms import PostForm, CommentForm
from .models import Post,by_user,Like,Comment,UserFollowing
from django.conf import settings
import json
from users.models import Profile

@login_required
def user_profile(request,user):
    profile = Profile.objects.get(username = user)
    following = UserFollowing.objects.filter(user = profile).count()
    followers = UserFollowing.objects.filter(following = profile).count()
    form = PostForm()

    ctx ={
        'profile':profile,
        'followers':followers,
        'following':following,
        'form':form
    }
    return render(request, 'post/user_profile.html',ctx)

@login_required
def home(request):
    data = by_user(request.user)
    context = {
        'data':data,
    }
    form = PostForm()
    context['form'] = form
    return render(request, 'post/dashboard.html',context)

@login_required
def post_detail(request,user,post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post = post_id)
    form = PostForm()
    comment = CommentForm()
    ctx = {
        'post':post,
        'comments':comments,
        'form':form,
        'comment':comment
    }
    return render(request,'post/post_detail.html',ctx)

def new_comment(request,post_id):
    if request.is_ajax and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            poster = request.user
            form.poster = poster
            post = get_object_or_404(Post,id=post_id)
            form.post = post
            form.save()
            instance = Post.objects.filter(poster=poster).filter(comments__isnull=True).first()
            ser_instance = serializers.serialize('json',[instance,])
            return JsonResponse({'instance':ser_instance},status = 200)
        else:
            return JsonResponse({'error':form.errors},status = 400)
    return JsonResponse({'error':''},status = 400)


def add_post(request):
    if request.is_ajax and request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            poster = request.user
            form.poster = poster
            form.save()
            instance = Post.objects.filter(poster=poster).first()
            ser_instance = serializers.serialize('json',[instance,])
            return JsonResponse({'instance':ser_instance},status = 200)
        else:
            return JsonResponse({'error':form.errors},status = 400)
    return JsonResponse({'error':''},status = 400)


@login_required
@require_POST
def like(request):
    if request.method == 'POST':
        user = request.user
        post_id = request.POST.get('id')
        post = get_object_or_404(Post,id=post_id)
        like = Like(post=post,liker=user)
        like.save()
        ctx = {'likes_count':like.post.like_count}
        return JsonResponse({'likes_count':like.post.like_count()})

@login_required
@require_POST
def unlike(request):
    if request.method == 'POST':
        user = request.user
        post_id = request.POST.get('id')
        post = get_object_or_404(Post,id=post_id)
        like = get_object_or_404(Like,post=post,liker=user)
        like.delete()
        ctx = {'likes_count':like.post.like_count}
        return JsonResponse({'likes_count':like.post.like_count()})