from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from .models import Post
from django.views.generic import (
ListView,
DetailView,
CreateView,
UpdateView,
DeleteView,)
# Create your views here.
def home(request):
    context = {
    'posts':Post.objects.all()   
    }
    return render(request,'blog/home.html',context=context)

def about(request):
    return render(request, "blog/about.html", {"title": "About"})

class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = ['-date_posted']
    paginate_by = 3


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User,username = self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']


    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']


    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def delete(self,*args,**kwargs):
        messages.success(self.request,"Post deleted successfully.")
        return super().delete(self,kwargs["pk"]) 

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

