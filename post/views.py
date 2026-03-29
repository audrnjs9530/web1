from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from post.forms import PostForm, CommentForm
from django.db.models import F
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from post.models import Post, Comment, Board


class BoardListView(View):
    def get(self, request):
        boards = Board.objects.all()
        return render(request, 'board_list.html', {'boards': boards})


class PostListView(View):
    def get(self, request, board_id):
        board = get_object_or_404(Board, id=board_id)
        posts_all = Post.objects.all().filter(board=board).order_by('-created_at')

        paginator = Paginator(posts_all, 10)
        page_number = request.GET.get('page', 1)
        posts = paginator.get_page(page_number)

        context = {'posts': posts, 'form': PostForm, 'board': board}

        return render(request, 'post_list.html', context)


class PostCreateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, board_id):
        board = get_object_or_404(Board, id=board_id)
        context = {'form': PostForm, 'board': board}
        return render(request, 'post_create.html', context)

    def post(self, request, board_id):
        board = get_object_or_404(Board, id=board_id)
        form = PostForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            author = request.user

            post = Post.objects.create(
                title=title,
                content=content,
                author=author,
                board=board
            )

            return render(request, 'post_detail.html', {'post': post})

        else:
            return redirect('posts', board_id=board_id)


class PostDetailView(View):
    def get(self, request, board_id, post_id):
        post = get_object_or_404(Post, id=post_id)
        is_liked = post.likes.filter(id=request.user.id).exists()
        comments = post.comments.order_by('-created_at')
        comment_form = CommentForm()
        context = {
            'post': post,
            'board_id': board_id,
            'is_liked': is_liked,
            'comments': comments,
            'comment_form': comment_form,
        }
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









# 댓글 작성
class CommentCreateView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
        return redirect('post', post_id=post_id)

# 댓글 삭제
class CommentDeleteView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, author=request.user)
        post_id = comment.post.id
        comment.delete()
        return redirect('post', post_id=post_id)

# 댓글 좋아요
class CommentLikeView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
        return redirect('post', post_id=comment.post.id)
