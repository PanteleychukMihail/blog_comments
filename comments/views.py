from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView

from comments.forms import CommentForm, LoginUserForm
from comments.models import Comment
from comments.utils import get_sort_params, get_sorted_comments, flatten_comments


class CommentListView(ListView):
    """View for displaying a list of comments.
        ListView for display paginated and sorted comments. Supports sorting by username, email, and created_at fields.
        """
    model = Comment
    template_name = 'comments/comment_list.html'
    context_object_name = 'root_comments'
    form_class = CommentForm
    ordering = ['-created_at']
    paginate_by = 25

    def get_queryset(self):
        """Get the queryset of comments, sorted based on request parameters.
        """
        sort_by, sort_direction = get_sort_params(self.request)
        queryset = get_sorted_comments(sort_by, sort_direction)
        return flatten_comments(queryset)

    def get_context_data(self, **kwargs):
        """Get context data for rendering the template.
            """
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()

        page = self.request.GET.get('page')
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        context['root_comments'] = paginator.get_page(page)

        return context


@method_decorator(login_required, name='dispatch')
class AddCommentView(View):
    """View for adding a new comment.
        """

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
            comment.username = request.user
            comment.save()
            return redirect('comment_list')
        return render(request, 'comments/add_comment.html', {'form': form})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to add comments.")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)


class EditCommentView(View):
    """View for editing an existing comment.
        """
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.username != request.user:
            messages.error(request, "You can only edit your comment.")
            return redirect('comment_list')
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
    """View for deleting an existing comment.
        """
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        if comment.username != request.user:
            messages.error(request, "You can only delete your comment.")
            return redirect('comment_list')
        return render(request, 'comments/confirm_delete.html', {'comment': comment})

    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        return redirect('comment_list')


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'comments/register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comment_list')
        return render(request, 'comments/register.html', {'form': form})


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'comments/login.html'

    def get_success_url(self):
        return reverse_lazy('comment_list')


def logout_user(request):
    logout(request)
    return redirect('comment_list')
