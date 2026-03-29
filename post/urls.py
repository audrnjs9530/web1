from django.urls import path
from post import views

urlpatterns = [
    # 게시판 목록
    path('', views.BoardListView.as_view(), name='boards'),

    # 게시판별 글 목록
    path('<int:board_id>/', views.PostListView.as_view(), name='posts'),

    # 글 작성
    path('<int:board_id>/create/', views.PostCreateView.as_view(), name='post_create'),

    # 글 상세
    path('<int:board_id>/post/<int:post_id>/', views.PostDetailView.as_view(), name='post'),

    # 글 좋아요
    path('<int:board_id>/post/<int:post_id>/like/', views.PostLikeView.as_view(), name='post_like'),

    # 글 삭제
    path('<int:board_id>/post/<int:post_id>/delete', views.PostDeleteView.as_view(), name='post_delete'),

    # 댓글 작성
    path('<int:board_id>/post/<int:post_id>/comment/', views.CommentCreateView.as_view(), name='comment_create'),

    # 댓글 삭제
    path('comment/<int:comment_id>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),

    # 댓글 좋아요
    path('comment/<int:comment_id>/like/', views.CommentLikeView.as_view(), name='comment_like'),
]