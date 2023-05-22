from django.urls import path, include
from polls import views as polls_views
from . import views
from django.contrib.auth import views as auth_views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/', views.AccountsView, name = 'accounts'),
    path('accounts/change_password', views.change_password, name='change_password'),

]
