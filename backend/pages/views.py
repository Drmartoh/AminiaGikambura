from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from projects.models import Project
from events.models import Event
from gallery.models import GalleryItem
from sports.models import SportProgram, Team
from reports.models import Report, ContactMessage

from .forms import RegisterForm, ContactForm

User = get_user_model()


# ---------- Page views (template-based) ----------

def home(request):
    featured_projects = Project.objects.filter(is_featured=True, status='ongoing')[:3]
    upcoming_events = Event.objects.filter(is_published=True).order_by('start_date')[:3]
    context = {
        'featured_projects': featured_projects,
        'upcoming_events': upcoming_events,
        'stats': {
            'members': 250,
            'projects': 45,
            'events': 120,
            'communities': 15,
        },
    }
    return render(request, 'pages/home.html', context)


def about(request):
    from projects.models import Project
    from events.models import Event
    project_count = Project.objects.count() or 45
    event_count = Event.objects.count() or 120
    context = {
        'stats': {
            'members': 250,
            'projects': project_count,
            'events': event_count,
            'communities': 15,
        },
    }
    return render(request, 'pages/about.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data.get('phone', ''),
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
            )
            messages.success(request, 'Thank you! Your message has been sent.')
            return redirect('pages:contact')
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})


class ProjectListView(ListView):
    model = Project
    template_name = 'pages/projects.html'
    context_object_name = 'projects'
    paginate_by = 12

    def get_queryset(self):
        return Project.objects.filter(is_public=True).select_related('category').order_by('-created_at')


def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_public=True)
    return render(request, 'pages/project_detail.html', {'project': project})


class EventListView(ListView):
    model = Event
    template_name = 'pages/events.html'
    context_object_name = 'events'
    paginate_by = 12

    def get_queryset(self):
        return Event.objects.filter(is_published=True).order_by('-start_date')


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug, is_published=True)
    return render(request, 'pages/event_detail.html', {'event': event})


def gallery(request):
    items = GalleryItem.objects.filter(is_public=True).order_by('-created_at')[:48]
    return render(request, 'pages/gallery.html', {'items': items})


def sports(request):
    programs = SportProgram.objects.filter(is_active=True)
    teams = Team.objects.filter(is_active=True).select_related('sport_program')
    return render(request, 'pages/sports.html', {'programs': programs, 'teams': teams})


def reports_list(request):
    report_list = Report.objects.filter(is_public=True).order_by('-report_date')
    return render(request, 'pages/reports.html', {'reports': report_list})


# ---------- Auth ----------

class WebLoginView(LoginView):
    template_name = 'pages/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('pages:dashboard')


class WebLogoutView(LogoutView):
    next_page = reverse_lazy('pages:home')


def register(request):
    if request.user.is_authenticated:
        return redirect('pages:dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please wait for admin approval before you can log in.')
            return redirect('pages:register_success')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'pages/register.html', {'form': form})


def register_success(request):
    return render(request, 'pages/register_success.html')


@login_required(login_url=reverse_lazy('pages:login'))
def dashboard(request):
    return render(request, 'pages/dashboard.html', {'user': request.user})
