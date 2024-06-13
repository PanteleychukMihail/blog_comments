from django.contrib.auth.models import User
from django.db import models


class Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    homepage = models.URLField(blank=True, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    def get_descendants(self) -> list:
        """Recursively fetches all descendants (replies) of the current comment.
        """
        descendants: list = list(self.replies.all())
        for reply in descendants:
            descendants.extend(reply.get_descendants())
        return descendants

