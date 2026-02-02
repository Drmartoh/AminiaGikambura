from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('projects/', views.ProjectListView.as_view(), name='projects'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('events/', views.EventListView.as_view(), name='events'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('sports/', views.sports, name='sports'),
    path('reports/', views.reports_list, name='reports'),
    path('login/', views.WebLoginView.as_view(), name='login'),
    path('logout/', views.WebLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('register/success/', views.register_success, name='register_success'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
