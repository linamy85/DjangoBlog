from django.shortcuts import render , get_object_or_404 , redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm

# Create your views here.

def post_list( req ):
    posts = Post.objects.filter( published_date__lte = timezone.now() ).order_by( 'published_date' )
    return render( req, 'blog/post_list.html', { 'posts': posts } )

def post_detail( req , pk ):
    post = get_object_or_404( Post , pk=pk )
    return render( req , 'blog/post_detail.html' , { 'post' : post } )

def post_new( req ):
    if req.method == "POST":
        form = PostForm( req.POST )
        if form.is_valid():
            post = form.save( commit = False ) # because we want to add author, so not commit first
                                               # but most of the time, we commit it first
            post.author = req.user
            post.published_date = timezone.now()
            post.save()
            return redirect( 'blog.views.post_detail' , pk = post.pk )
    else:
        form = PostForm()
    return render( req , 'blog/post_edit.html' , { 'form' : form } )

def post_edit( req , pk ):
    post = get_object_or_404( Post , pk=pk )
    if req.method == "POST":
        form = PostForm(req.POST, instance=post)
        if form.is_valid():
            post = form.save( commit = False )
            post.author = req.user
            post.published_date = timezone.now()
            post.save()
            return redirect( 'blog.views.post_detail' , pk=post.pk )
    else:
        form = PostForm( instance=post )
    return render( req , 'blog/post_edit.html' , { 'form' : form } )


