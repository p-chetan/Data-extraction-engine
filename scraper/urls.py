from os import name
from scraper.forms import LoginForm,MyPasswordChange, PasswordResetForm, SetPassword, LoginForm
from django.contrib import admin
from django.urls import path
from scraper import views  
from .views import json
from django.contrib.auth import authenticate, views as auth_views

urlpatterns = [
    path("", views.index,name='home'),
    path("index",views.index,name='home'),
    path("store", views.store,name='store'),
    path("about", views.about,name='about'),
    
    path("signup", views.SignupView.as_view(),name='signup'),
    path("login", auth_views.LoginView.as_view(template_name='login.html',authentication_form=LoginForm), name='login'),
    path('logout',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('accounts/profile/', views.profile, name='profile'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='passwordchange.html',form_class=MyPasswordChange, success_url='/passwordchangedone/'),name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='passwordchangedone.html'),name='passwordchangedone'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='password_reset.html',form_class=PasswordResetForm),name='password_reset'),
    path('password-reset-done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=SetPassword),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),

    path("json",views.json,name="json"),    
    path("edit/<int:id>", views.edit),
    path("editbuzz/<int:id>",views.editbuzz),
    path("editpdf/<int:id>",views.editpdf),

    path("delete/<int:id>", views.delete),
    path("deletebuzz/<int:id>", views.deletebuzz),
    path("deletepdf/<int:id>", views.deletepdf),

    path("apply/<int:id>", views.apply),
    path("applybuzz/<int:id>", views.applybuzz),
    path("applypdf/<int:id>", views.applypdf),
    path("schedule1/<int:id>", views.schedule1),

    path('search',views.search),
    path('accounts/profile/search',views.search),

    path("finviz", views.finviz,name='finviz'),
    path("newO", views.newO,name='newO'),
    

    path('Invest',views.Invest),
    path('buzz',views.buzz),
    path("storebuzz", views.storebuzz,name='storebuzz'),

    path('pdf',views.pdf),
    path('pdf1',views.pdf1),
    path("storepdf", views.storepdf,name='storepdf'),
    path("naming",views.naming),
]

