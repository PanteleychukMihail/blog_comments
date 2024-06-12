from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from comments.forms import CommentForm
from comments.models import Comment


class CommentListView(View):
    form = CommentForm()

    def get(self, request):
        form = self.form
        sort_by = request.GET.get('sort_by', 'created_at')
        sort_direction = request.GET.get('sort_direction', 'desc')
        sortable_fields = ['username', 'email', 'created_at']

        if sort_by not in sortable_fields:
            sort_by = 'created_at'

        if sort_direction == 'asc':
            sort_field = sort_by
        else:
            sort_field = '-' + sort_by

        root_comments = Comment.objects.filter(parent=None).order_by(sort_field)

        return render(request, 'comments/comment_list.html',
                      {'root_comments': root_comments, 'form': form})


class AddCommentView(View):
    def get(self, request, parent_id=None):
        parent = get_object_or_404(Comment, id=parent_id) if parent_id else None
        form = CommentForm(initial={'parent': parent})
        return render(request, 'comments/add_comment.html', {'form': form})

    def post(self, request, parent_id=None):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            if parent_id:
                comment.parent = get_object_or_404(Comment, id=parent_id)
            comment.save()
            return redirect('comment_list')
        return render(request, 'comments/add_comment.html', {'form': form})


class EditCommentView(View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        form = CommentForm(instance=comment)
        return render(request, 'comments/edit_comment.html', {'form': form, 'comment': comment})

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('comment_list')
        return render(request, 'comments/edit_comment.html', {'form': form, 'comment': comment})


class DeleteCommentView(View):
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        return render(request, 'comments/confirm_delete.html', {'comment': comment})

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        return redirect('comment_list')
