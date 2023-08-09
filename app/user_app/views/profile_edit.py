from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from user_app.models import CustomUser, UserProfileInfo, ProfileBanner
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required


class ProfilePicUpdateView(LoginRequiredMixin, UpdateView):
    """
    View class to update the user's profile picture.

    Inherits from:
        LoginRequiredMixin: Mixin to require user login before accessing the view.
        UpdateView: Built-in view class for updating a model instance.

    Attributes:
        model (Model): The model to update (UserProfileInfo).
        fields (list): List of fields to be updated (profile_pic).
    
    Methods:
        form_valid(form): Override method to associate the user with the updated instance.
        get_success_url(): Method to determine the URL to redirect after successful form submission.
    """
    model = UserProfileInfo
    fields = ['profile_pic']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user_app:profile_redirect')


class ProfileBannerUpdateView(LoginRequiredMixin, UpdateView):
    """
    View class to update the user's profile banner.

    Inherits from:
        LoginRequiredMixin: Mixin to require user login before accessing the view.
        UpdateView: Built-in view class for updating a model instance.

    Attributes:
        model (Model): The model to update (ProfileBanner).
        fields (list): List of fields to be updated (profile_banner).
    
    Methods:
        form_valid(form): Override method to associate the user with the updated instance.
        get_success_url(): Method to determine the URL to redirect after successful form submission.
    """
    model = ProfileBanner
    fields = ['profile_banner']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('user_app:profile_redirect')
    

class BiographyUpdateView(LoginRequiredMixin, UpdateView):
    """
    View class to update the user's biography.

    Inherits from:
        LoginRequiredMixin: Mixin to require user login before accessing the view.
        UpdateView: Built-in view class for updating a model instance.

    Attributes:
        model (Model): The model to update (CustomUser).
        fields (list): List of fields to be updated (biography).

    Methods:
        get_object(queryset): Override method to fetch the current user's profile for updating.
        get_success_url(): Method to determine the URL to redirect after successful form submission.
    """
    model = CustomUser
    fields = ['biography']

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_success_url(self):
        return reverse('user_app:profile_redirect')


@login_required
def delete_profile_pic(request, pk):
    """
    Delete the profile picture of the user.
    Requires the user to be logged in to access the view.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the user's UserProfileInfo instance.

    Returns:
        HttpResponse: Redirects to the user's profile page.
    """
    user_profile = get_object_or_404(UserProfileInfo, pk=pk)

    if pk == request.user.userprofileinfo.id:
        user_profile.profile_pic.delete()

    return redirect(reverse('user_app:profile_redirect'))


