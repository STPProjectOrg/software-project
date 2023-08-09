""" Functions related to the user authentification. """

from django.urls import reverse_lazy
from django.shortcuts import render
from user_app.models import UserProfileInfo, ProfileBanner
from user_app.forms import UserRegistrationForm
from settings_app.models import Settings
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin


def register(request):
    """
    View function for user registration.

    This function handles user registration by processing the form data submitted via POST request.
    If the form data is valid, a new user is created and saved to the database.
    If the registration is successful, the user is redirected to a success page.

    Args:
        request (HttpRequest): The HTTP request object containing the form data.

    Returns:
        HttpResponse: A rendered HTML template with user registration form or a success page.
    """
    if request.method == "POST":
        # Get the form data of the POST-method
        user_form = UserRegistrationForm(data=request.POST)

        if user_form.is_valid():

            # Save the user registration data from POST-form to the database and hash the password
            new_user = user_form.save()
            new_user.set_password(new_user.password)
            new_user.save()

            # Create new model instances for ProfileInfo, Settings and Banner and asign
            # the new created CustomUser instance as foreign key  
            UserProfileInfo.objects.create(user=new_user)
            Settings.objects.create(user=new_user)
            ProfileBanner.objects.create(user=new_user)

            # Render the success page
            return render(request, 'user_app/register/registration_success.html')

    else:
        # Get the blank Registration Form
        user_form = UserRegistrationForm()

    # Render the registration Page 
    return render(request, 'user_app/register/registration.html',
                  {'user_form': user_form})


def register_success(request):
    """ View function to render the registration success page."""
    return render(request, 'user_app/register/registration_succsess.html')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    View class to handle the password reset process.

    Inherits from:
        SuccessMessageMixin: Mixin to display a success message after password reset.
        PasswordResetView: Built-in view class for password reset.

    Attributes:
        template_name (str): HTML template for displaying the password reset form.
        email_template_name (str): HTML email template for the password reset email.
        subject_template_name (str): Subject template for the password reset email.
        success_url (str): URL to redirect after a successful password reset.
    """
    template_name = 'users/password_reset.html'
    email_template_name = "user_app/password_recovery/reset_password_email.html",
    subject_template_name = "user_app/password_recovery/reset_password_email_subject",
    success_url = reverse_lazy('user_app:password_reset_done')


class ConfirmResetPasswordView(PasswordResetConfirmView):
    """
    View class to confirm the password reset process.

    Inherits from:
        PasswordResetConfirmView: Built-in view class for confirming password reset.

    Attributes:
        success_url (str): URL to redirect after successfully confirming password reset.

    """
    success_url = reverse_lazy('user_app:password_reset_complete')