
from django.conf import settings
from django.urls import reverse
from django.db import models
from django.utils.text import slugify              #to remove faltu words space etc
# from accounts.models import User

import misaka             #to do link embedding

from django.contrib.auth import get_user_model    #returns user model currently active
User = get_user_model()

# https://docs.djangoproject.com/en/1.11/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag
from django import template
register = template.Library()           #to use custom templates



class Group(models.Model):
    name = models.CharField(max_length=255, unique=True) #name of group
    slug = models.SlugField(allow_unicode=True, unique=True) #group will have a slug
    description = models.TextField(blank=True, default='')  #group ka description
    description_html = models.TextField(editable=False, default='', blank=True) #html version of description
    members = models.ManyToManyField(User,through="GroupMember")

    def __str__(self):    #string representation of group object
        return self.name

    def save(self, *args, **kwargs):  #to save a group
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):  #return a reverse calls of group single
        return reverse("groups:single", kwargs={"slug": self.slug})


    class Meta:
        ordering = ["name"]


class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name="memberships",on_delete=models.PROTECT) #group member is linked to the group class through this foreign key
    user = models.ForeignKey(User,related_name='user_groups',on_delete=models.PROTECT)

    def __str__(self):   #string method
        return self.user.username

    class Meta:
        unique_together = ("group", "user")   #

# Create your models here.
