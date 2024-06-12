from django.urls import path

from comments.views import CommentListView, AddCommentView, EditCommentView, DeleteCommentView

urlpatterns = [
    path('', CommentListView.as_view(), name='comment_list'),
    path('add/', AddCommentView.as_view(), name='add_comment'),
    path('edit/<int:comment_id>/', EditCommentView.as_view(), name='edit_comment'),
    path('delete/<int:comment_id>/', DeleteCommentView.as_view(), name='delete_comment'),
    path('reply/<int:parent_id>/', AddCommentView.as_view(), name='reply_comment'),
]
