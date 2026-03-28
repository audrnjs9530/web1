from django.urls import path
from post import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='posts'),
    path('create/', views.PostCreateView.as_view(), name='post_create'),
    path('<int:post_id>/', views.PostDetailView.as_view(), name='post'), # 상세 게시글 조회
    path('<int:post_id>/like/', views.PostLikeView.as_view(), name='post_like'),
    path('post/<int:post_id>/comment/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:comment_id>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/<int:comment_id>/like/', views.CommentLikeView.as_view(), name='comment_like'),

]