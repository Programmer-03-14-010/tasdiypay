from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("", views.landing_view, name="landing"),
    path("register/", views.register_view, name="register"),
    path("login/", views.NameLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="landing"), name="logout"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("pay/", views.pay_view, name="pay"),
    path("my-payments/", views.my_payments_view, name="my_payments"),
    path("my-payments/<int:pk>/", views.payment_detail_view, name="payment_detail"),
    path("profile/", views.profile_view, name="profile"),
    path("staff-panel/", views.staff_login_redirect, name="staff_login_redirect"),
]
