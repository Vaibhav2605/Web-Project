from django.contrib import messages
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from django.urls import reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic
from groups.models import Group,GroupMember
from . import models

class CreateGroup(LoginRequiredMixin, generic.CreateView): #to create a group uska view (jo dikhega )
    fields = ("name", "description")
    model = Group

class SingleGroup(generic.DetailView): #detail of the group
    model = Group

class ListGroups(generic.ListView): #list of all the groups
    model = Group


class JoinGroup(LoginRequiredMixin, generic.RedirectView):  #to join group

    def get_redirect_url(self, *args, **kwargs):  #to grab whatever url they want to connect to
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):   #if we dont get object then it will return error 404
        group = get_object_or_404(Group,slug=self.kwargs.get("slug"))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)

        except IntegrityError:
            messages.warning(self.request,("Warning, you are already a member of {}".format(group.name))) #checking if user already a member

        else:
            messages.success(self.request,"You are now a member of the {} group.".format(group.name))

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:

            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you are not a member of it yet!"
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)
