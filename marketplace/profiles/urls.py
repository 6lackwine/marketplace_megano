from django.conf.urls.static import static
from django.urls import path

from django.conf import settings
from profiles.views import ProfileAPIView, SignUpAPIView, sign_in, sign_out, ProfileAvatarAPIView, \
    ProfilePasswordAPIView

urlpatterns = [
    path("profile", ProfileAPIView.as_view(), name="my_profile"),
    path("profile/avatar", ProfileAvatarAPIView.as_view(), name="profile_avatar"),
    path("profile/password", ProfilePasswordAPIView.as_view(), name="password"),
    path("sign-up", SignUpAPIView.as_view(), name="register_profile"),
    path("sign-out", sign_out, name="logout"),
    path("sign-in", sign_in, name="login"),
]