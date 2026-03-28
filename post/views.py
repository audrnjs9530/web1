from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from post.forms import PostForm
from django.db.models import F
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from post.models import Post

class PostListView(View):
    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        context = {'posts': posts, 'form': PostForm}
        return render(request, 'post_list.html', context)


class PostCreateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        context = {'form': PostForm}
        return render(request, 'post_create.html', context)

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            author = request.user

            post = Post.objects.create(
                title=title,
                content=content,
                author=author,
            )

            return render(request, 'post_detail.html', {'post': post})

        else:
            return redirect('posts')


class PostDetailView(View):
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        is_liked = post.likes.filter(id=request.user.id).exists()
        context = {'post': post, 'is_liked': is_liked}
        return render(request, 'post_detail.html', context)

class PostLikeView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)  # 취소
        else:
            post.likes.add(request.user)

        is_liked = post.likes.filter(id=request.user.id).exists()
        context = {'post': post, 'is_liked': is_liked}
        return render(request, 'post_detail.html', context)
