from django.conf import settings
from django.urls import reverse
from django.db import models

import misaka   #to write markdown in their actual posts

from groups.models import  Group  #to connect post to group

from django.contrib.auth import get_user_model  #to connect the post to the currently logged in user
User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, related_name="posts",on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False) #so that people cant edit the html feild
    group = models.ForeignKey(Group, related_name="posts",null=True, blank=True,on_delete=models.PROTECT)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "posts:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk    #primary key
            }
        )

    class Meta:
        ordering = ["-created_at"]  #- sign to dat we can see in decending order
        unique_together = ["user", "message"]
