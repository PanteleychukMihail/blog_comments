from django.db import models


class Comment(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    homepage = models.URLField(blank=True, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    def get_descendants(self):
        descendants = list(self.replies.all())
        for reply in descendants:
            descendants.extend(reply.get_descendants())
        return descendants

