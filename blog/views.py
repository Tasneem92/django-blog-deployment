from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from blog.models import Post,Comment
from blog.forms import PostForm,CommentForm
from django.urls import reverse_lazy # it waits until I delete the post until it view the url

 # zay el decorator ta3 el functions based view bas lal classes based view
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView)
# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post

    # define how to grab posts list
    # queryset allows to me to use Django ORM when dealing with generic views
    # to add a custom touch to ORM
    # SQL query on my model that grabs the post model objects and filter it based on my condition
    # published_date__lte: grabs published_date
    # and after __ you write the field condition
    # lte is a condition : less than or equal to
    # -published_date : the dash (-) orders them in descending order, the most recent blog posts comes up front
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
    # I don't anyone to be able to access this CreatePostView
    # Mixins attributes
    # Specifies where the login url should be
    login_url = '/login/'
    # redirect field :
    redirect_field_name = 'blog/post_detail.html'

    form_class = PostForm

    model = Post

# Decorators work with functions based view only

# if I wanna update sth I should be logged in so I use LoginRequiredMixin
class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm

    model = Post

class PostDDeleteView(LoginRequiredMixin,DeleteView):
    # Connecting to the model I'll be deleting from
    model = Post
    # I don't want to activate success_url unless it's deleted
    # redirect to homepage
    success_url = reverse_lazy('post_list')

# A view that lists my unpublished drafts
class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    # make sure there is no publication date on it
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('-create_date')


#############################################
#############################################
@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk) # 404 if not found
    if request.method == 'POST': # someone filled in the form, hit enter
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
    return render(request,'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)
