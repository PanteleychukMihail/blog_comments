from typing import Tuple, List

from .models import Comment


def get_sort_params(request) -> Tuple[str, str]:
    """Extracts sorting parameters from the request's GET parameters.
    """
    sort_by = request.GET.get('sort_by', 'created_at')
    sort_direction = request.GET.get('sort_direction', 'desc')
    sortable_fields = ['username', 'email', 'created_at']

    if sort_by not in sortable_fields:
        sort_by = 'created_at'

    if sort_direction not in ['asc', 'desc']:
        sort_direction = 'desc'

    return sort_by, sort_direction


def get_sorted_comments(sort_by: str, sort_direction: str) -> List[Comment]:
    """ Retrieves sorted root comments based on provided sorting parameters.
    """
    if sort_direction == 'asc':
        sort_field = sort_by
    else:
        sort_field = '-' + sort_by

    return Comment.objects.filter(parent=None).order_by(sort_field)


def flatten_comments(comments: List[Comment], level: int = 0) -> List[Tuple[int, Comment]]:
    """Flattens nested comments into a list with tuples indicating comment level.
    """
    flat_comments: List[Tuple[int, Comment]] = []
    for comment in comments:
        flat_comments.append((level, comment))
        flat_comments.extend(flatten_comments(comment.replies.all(), level + 1))
    return flat_comments
