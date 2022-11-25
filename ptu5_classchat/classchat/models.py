from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Group(models.Model):
    name = models.CharField(_("group name"), max_length=50)


class Subject(models.Model):
    name = models.CharField(_("subject name"), max_length=50)
    group = models.ForeignKey(
        Group, 
        verbose_name=_("group"), 
        on_delete=models.CASCADE,
        related_name='subjects',
    )


class Post(models.Model):
    title = models.CharField(_("title"), max_length=50)
    body = models.TextField(_("body"))
    subject = models.ForeignKey(
        Subject, 
        verbose_name=_("subject"), 
        on_delete=models.CASCADE,
        related_name='posts',
        )
    user = models.ForeignKey(
        User, 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name='posts', 
        )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    def __str__(self) -> str:
        return _("For {subject} about {title} by {user} posted at {created_at}").format(
            subject=self.subject,
            title=self.title,
            user=self.user,
            created_at=self.created_at,
        )

    class Meta:
        ordering = ('-created_at', )


class PostComment(models.Model):
    user = models.ForeignKey(
        User, 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name='post_comments'
        )
    post = models.ForeignKey(
        Post, 
        verbose_name=_("post"), 
        on_delete=models.CASCADE,
        related_name='post_comments',
        )
    post_comment = models.TextField(_("post comment"))
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)


    def __str__(self) -> str:
        return _("{post_comment} by {user} posted at {created_at}").format(
            post_comment=self.post_comment,
            user=self.user,
            created_at=self.created_at,
        )
    
    class Meta:
        ordering = ('-created_at', )


