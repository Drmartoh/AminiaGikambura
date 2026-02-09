import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from projects.models import Project
from events.models import Event
from gallery.models import GalleryItem
from sports.models import SportProgram, Team
from reports.models import Report, ContactMessage
from core.models import Constituency, Ward, Official, YouthJob, AboutPage

from .forms import RegisterForm, ContactForm, DonorRegisterForm, CountyOfficialRegisterForm

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
    about_content = AboutPage.load()
    context = {
        'stats': {
            'members': 250,
            'projects': project_count,
            'events': event_count,
            'communities': 15,
        },
        'about_content': about_content,
    }
    return render(request, 'pages/about.html', context)


def officials(request):
    """Public Officials page (CBO leadership)."""
    items = Official.objects.filter(is_published=True).order_by('order', 'name')
    return render(request, 'pages/officials.html', {'officials': items})


def youth_jobs(request):
    """Public Community Youth Jobs / opportunities page."""
    items = YouthJob.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'pages/youth_jobs.html', {'jobs': items})


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

    def form_valid(self, form):
        """Reject donors/county officials until approved/verified; only admins see Manage."""
        user = form.get_user()
        if user.role == 'donor' and not user.is_approved:
            from django.contrib.auth import logout
            logout(self.request)
            messages.error(self.request, 'Your donor account is pending approval. You will be able to log in once an admin approves you.')
            return redirect('pages:login')
        if user.role == 'county_official' and not user.is_verified:
            from django.contrib.auth import logout
            logout(self.request)
            messages.error(self.request, 'Your county official account is pending verification. You will be able to log in once verified.')
            return redirect('pages:login')
        return super().form_valid(form)

    def get_success_url(self):
        if getattr(self.request.user, 'is_admin_user', False):
            return reverse_lazy('manage:dashboard')
        return super().get_success_url()


class WebLogoutView(LogoutView):
    """Log out and always redirect to the public site home (no 'Logged out' page)."""
    next_page = reverse_lazy('pages:home')
    http_method_names = ['get', 'post', 'head', 'options']

    def get_success_url(self):
        return str(reverse_lazy('pages:home'))

    def get(self, request, *args, **kwargs):
        """Log out and redirect to home on GET (e.g. when clicking Log out link)."""
        logout(request)
        return redirect('pages:home')


def wards_json(request):
    """API: wards by constituency_id for registration form."""
    cid = request.GET.get('constituency_id')
    if not cid:
        return JsonResponse({})
    wards = list(Ward.objects.filter(constituency_id=cid).order_by('name').values('id', 'name'))
    return JsonResponse({'wards': wards})


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
    # For JS: constituency_id -> list of {id, name} wards
    wards_by_constituency = {}
    for c in Constituency.objects.prefetch_related('wards').order_by('order', 'name'):
        wards_by_constituency[str(c.id)] = [{'id': w.id, 'name': w.name} for w in c.wards.order_by('name')]
    return render(request, 'pages/register.html', {
        'form': form,
        'wards_by_constituency': json.dumps(wards_by_constituency),
    })


def register_success(request):
    return render(request, 'pages/register_success.html')


def donor_register(request):
    """Donor/Sponsor registration: name or company, email, phone, credentials. Admin approves after."""
    if request.user.is_authenticated:
        return redirect('pages:dashboard')
    if request.method == 'POST':
        form = DonorRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for registering as a donor/sponsor. Your account is pending approval. You will be able to log in once an admin approves you.')
            return redirect('pages:donor_register_success')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = DonorRegisterForm()
    return render(request, 'pages/donor_register.html', {'form': form})


def donor_register_success(request):
    return render(request, 'pages/donor_register_success.html')


def county_official_register(request):
    """County official registration: name, department, phone, email, password. Admin verifies after."""
    if request.user.is_authenticated:
        return redirect('pages:dashboard')
    if request.method == 'POST':
        form = CountyOfficialRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for registering. Your account is pending verification. You will be able to log in once verified.')
            return redirect('pages:county_official_register_success')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = CountyOfficialRegisterForm()
    return render(request, 'pages/county_official_register.html', {'form': form})


def county_official_register_success(request):
    return render(request, 'pages/county_official_register_success.html')


@login_required(login_url=reverse_lazy('pages:login'))
def dashboard(request):
    return render(request, 'pages/dashboard.html', {'user': request.user})
