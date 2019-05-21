from django.urls import path
from django.contrib.auth.decorators import login_required

from apps.fb import views

urlpatterns = [
    path('', login_required(views.HomePageView.as_view()), name='home'),
    path('deauth', login_required(views.DeauthView.as_view()), name='deauth'),
]
