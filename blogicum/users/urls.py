from django.contrib.auth import views as auth_views
from django.urls import include, path, reverse_lazy
from . import views

app_name = 'users'

urlpatterns = [
    path('', 
         include('django.contrib.auth.urls')),
    
    path('registration/',
         views.CreateUser.as_view(),
         name='registration'),
    
    path('password_change/',
         auth_views.PasswordChangeView.as_view(),
         name='password_change'),
    
     path(
        'password_reset/',
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy('users:password_reset_done')
        ),
        name='password_reset',
     ),

     path('logout/', auth_views.LogoutView.as_view(
          template_name='registration/logged_out.html',
          next_page='users:login'
     ), name='logout'),

     path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('users:password_reset_complete')
        ),
        name='password_reset_confirm',
    ),

    path('account/edit/',
         views.UpdateProfile.as_view(),
         name='edit_profile'),
]
