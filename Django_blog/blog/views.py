from django.shortcuts import render
from .models import Post
from django.views.generic import (ListView,DeleteView,
                                  DetailView,UpdateView,
                                  CreateView)
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title','content']

    #associating a user to the created form
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['title','content']

    #associating a user to the created form
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    #Userpassestest mixin runs this function to validate the user
    def test_func(self):
        current_post = self.get_object()
        if self.request.user==current_post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = '/'

    # Userpassestest mixin runs this function to validate the user
    def test_func(self):
        current_post = self.get_object()
        if self.request.user == current_post.author:
            return True
        else:
            return False