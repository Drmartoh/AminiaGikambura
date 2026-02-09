"""Custom admin / manage area views (eye-catching UI, no Django admin)."""
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils import timezone
from django.utils.text import slugify

from core.models import SiteSettings, AuditLog, Official, YouthJob, AboutPage, SectionStyle, SectionSlide
from gallery.models import GalleryItem
from reports.models import ContactMessage
from projects.models import Project
from events.models import Event
from sports.models import SportProgram, Team
from .forms import (
    SiteSettingsForm, GalleryItemForm, ProjectForm, EventForm,
    SportProgramForm, TeamForm, AboutPageForm, OfficialForm, YouthJobForm,
    UserCreateForm, UserEditForm, SectionStyleForm, SectionSlideForm,
)

User = get_user_model()


def require_admin(view_func):
    """Decorator: require login and admin/super_admin role. Redirect to login or dashboard."""
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('pages:login')  # use main site login
        if not getattr(request.user, 'is_admin_user', False):
            return redirect('pages:dashboard')  # members see normal dashboard
        return view_func(request, *args, **kwargs)
    return wrapped


@require_admin
def dashboard(request):
    """Manage dashboard home: stats and quick links."""
    pending = User.objects.filter(role='member', is_approved=False).count()
    total_members = User.objects.filter(role='member', is_approved=True).count()
    gallery_count = GalleryItem.objects.filter(is_public=True).count()
    projects_count = Project.objects.filter(is_public=True).count()
    events_count = Event.objects.filter(is_published=True).count()
    officials_count = Official.objects.filter(is_published=True).count()
    youth_jobs_count = YouthJob.objects.filter(is_published=True).count()
    recent_messages = ContactMessage.objects.order_by('-created_at')[:5]
    return render(request, 'pages/manage/dashboard.html', {
        'pending_members': pending,
        'total_members': total_members,
        'gallery_count': gallery_count,
        'projects_count': projects_count,
        'events_count': events_count,
        'officials_count': officials_count,
        'youth_jobs_count': youth_jobs_count,
        'recent_messages': recent_messages,
    })


@require_admin
def members_list(request):
    """List members with approve/reject actions."""
    pending = User.objects.filter(role='member', is_approved=False).select_related('ward', 'ward__constituency').order_by('-date_joined')
    approved = User.objects.filter(role='member', is_approved=True).select_related('ward', 'ward__constituency').order_by('-date_joined')[:50]
    return render(request, 'pages/manage/members.html', {
        'pending': pending,
        'approved': approved,
    })


@require_admin
def member_approve(request, pk):
    """Approve a member."""
    user = get_object_or_404(User, pk=pk, role='member')
    user.is_approved = True
    user.save(update_fields=['is_approved', 'updated_at'])
    AuditLog.objects.create(
        user=request.user,
        action='approve',
        model_name='User',
        object_id=str(user.pk),
        object_repr=str(user),
        ip_address=get_client_ip(request),
    )
    messages.success(request, f'{user.username} has been approved.')
    return redirect('manage:members')


@require_admin
def member_reject(request, pk):
    """Reject / unapprove a member."""
    user = get_object_or_404(User, pk=pk, role='member')
    user.is_approved = False
    user.save(update_fields=['is_approved', 'updated_at'])
    AuditLog.objects.create(
        user=request.user,
        action='reject',
        model_name='User',
        object_id=str(user.pk),
        object_repr=str(user),
        ip_address=get_client_ip(request),
    )
    messages.success(request, f'{user.username} has been unapproved.')
    return redirect('manage:members')


def get_client_ip(request):
    xff = request.META.get('HTTP_X_FORWARDED_FOR')
    if xff:
        return xff.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR') or None


@require_admin
def gallery_list(request):
    """List gallery items with edit/delete links."""
    items = GalleryItem.objects.all().order_by('-created_at')[:60]
    return render(request, 'pages/manage/gallery_list.html', {'items': items})


@require_admin
def gallery_add(request):
    """Add a gallery item."""
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.uploaded_by = request.user
            item.save()
            messages.success(request, 'Gallery item added.')
            return redirect('manage:gallery_list')
    else:
        form = GalleryItemForm(initial={'year': timezone.now().year, 'is_public': True})
    return render(request, 'pages/manage/gallery_form.html', {'form': form, 'title': 'Add gallery item'})


@require_admin
def gallery_edit(request, pk):
    """Edit a gallery item."""
    item = get_object_or_404(GalleryItem, pk=pk)
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Gallery item updated.')
            return redirect('manage:gallery_list')
    else:
        form = GalleryItemForm(instance=item)
    return render(request, 'pages/manage/gallery_form.html', {'form': form, 'item': item, 'title': 'Edit gallery item'})


@require_admin
def gallery_delete(request, pk):
    """Delete a gallery item."""
    item = get_object_or_404(GalleryItem, pk=pk)
    if request.method == 'POST':
        title = item.title
        item.delete()
        messages.success(request, f'"{title}" deleted.')
        return redirect('manage:gallery_list')
    return render(request, 'pages/manage/gallery_confirm_delete.html', {'item': item})


@require_admin
def settings_edit(request):
    """Edit site settings (singleton)."""
    obj = SiteSettings.load()
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Site settings saved.')
            return redirect('manage:settings')
    else:
        form = SiteSettingsForm(instance=obj)
    return render(request, 'pages/manage/settings.html', {'form': form, 'site_settings': obj})


@require_admin
def contact_messages(request):
    """List contact form messages."""
    messages_list = ContactMessage.objects.order_by('-created_at')[:100]
    return render(request, 'pages/manage/messages.html', {'messages_list': messages_list})


# ---------- Users ----------
@require_admin
def users_list(request):
    users = User.objects.all().select_related('ward').order_by('-date_joined')[:100]
    return render(request, 'pages/manage/users_list.html', {'users': users})


@require_admin
def user_add(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created.')
            return redirect('manage:users_list')
    else:
        form = UserCreateForm(initial={'role': 'member', 'is_active': True}, request=request)
    return render(request, 'pages/manage/user_form.html', {'form': form, 'title': 'Add user'})


@require_admin
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated.')
            return redirect('manage:users_list')
    else:
        form = UserEditForm(instance=user, request=request)
    return render(request, 'pages/manage/user_form.html', {'form': form, 'title': 'Edit user', 'edit_user': user})


@require_admin
def donors_list(request):
    """List donors with pending approval; approve action."""
    pending = User.objects.filter(role='donor', is_approved=False).order_by('-date_joined')
    approved = User.objects.filter(role='donor', is_approved=True).order_by('-date_joined')[:50]
    return render(request, 'pages/manage/donors.html', {
        'pending': pending,
        'approved': approved,
    })


@require_admin
def donor_approve(request, pk):
    """Approve a donor/sponsor."""
    user = get_object_or_404(User, pk=pk, role='donor')
    user.is_approved = True
    user.save(update_fields=['is_approved', 'updated_at'])
    AuditLog.objects.create(
        user=request.user,
        action='approve',
        model_name='User',
        object_id=str(user.pk),
        object_repr=str(user),
        ip_address=get_client_ip(request),
    )
    messages.success(request, f'{user.get_full_name() or user.username} has been approved as donor.')
    return redirect('manage:donors')


@require_admin
def county_officials_list(request):
    """List county officials with pending verification; verify action."""
    pending = User.objects.filter(role='county_official', is_verified=False).order_by('-date_joined')
    verified = User.objects.filter(role='county_official', is_verified=True).order_by('-date_joined')[:50]
    return render(request, 'pages/manage/county_officials.html', {
        'pending': pending,
        'verified': verified,
    })


@require_admin
def county_official_verify(request, pk):
    """Verify a county official."""
    user = get_object_or_404(User, pk=pk, role='county_official')
    user.is_verified = True
    user.save(update_fields=['is_verified', 'updated_at'])
    AuditLog.objects.create(
        user=request.user,
        action='verify',
        model_name='User',
        object_id=str(user.pk),
        object_repr=str(user),
        ip_address=get_client_ip(request),
    )
    messages.success(request, f'{user.get_full_name() or user.username} has been verified.')
    return redirect('manage:county_officials')


# ---------- Projects ----------
@require_admin
def projects_list(request):
    items = Project.objects.all().select_related('category', 'county').order_by('-created_at')[:80]
    return render(request, 'pages/manage/projects_list.html', {'items': items})


@require_admin
def project_add(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            if not obj.slug:
                obj.slug = slugify(obj.title)
            obj.created_by = request.user
            obj.save()
            messages.success(request, 'Project added.')
            return redirect('manage:projects_list')
    else:
        form = ProjectForm(initial={'is_public': True, 'status': 'planned'})
    return render(request, 'pages/manage/project_form.html', {'form': form, 'title': 'Add project'})


@require_admin
def project_edit(request, pk):
    obj = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated.')
            return redirect('manage:projects_list')
    else:
        form = ProjectForm(instance=obj)
    return render(request, 'pages/manage/project_form.html', {'form': form, 'title': 'Edit project', 'item': obj})


@require_admin
def project_delete(request, pk):
    obj = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        title = obj.title
        obj.delete()
        messages.success(request, f'"{title}" deleted.')
        return redirect('manage:projects_list')
    return render(request, 'pages/manage/confirm_delete.html', {'item': obj, 'cancel_url': 'manage:projects_list', 'label': 'project'})


# ---------- Events ----------
@require_admin
def events_list(request):
    items = Event.objects.all().order_by('-start_date')[:80]
    return render(request, 'pages/manage/events_list.html', {'items': items})


@require_admin
def event_add(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            if not obj.slug:
                obj.slug = slugify(obj.title)
            obj.created_by = request.user
            obj.save()
            messages.success(request, 'Event added.')
            return redirect('manage:events_list')
    else:
        form = EventForm(initial={'is_published': False, 'is_featured': False})
    return render(request, 'pages/manage/event_form.html', {'form': form, 'title': 'Add event'})


@require_admin
def event_edit(request, pk):
    obj = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated.')
            return redirect('manage:events_list')
    else:
        form = EventForm(instance=obj)
    return render(request, 'pages/manage/event_form.html', {'form': form, 'title': 'Edit event', 'item': obj})


@require_admin
def event_delete(request, pk):
    obj = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        title = obj.title
        obj.delete()
        messages.success(request, f'"{title}" deleted.')
        return redirect('manage:events_list')
    return render(request, 'pages/manage/confirm_delete.html', {'item': obj, 'cancel_url': 'manage:events_list', 'label': 'event'})


# ---------- Sports (programs & teams) ----------
@require_admin
def sport_programs_list(request):
    items = SportProgram.objects.all().order_by('name')
    return render(request, 'pages/manage/sport_programs_list.html', {'items': items})


@require_admin
def sport_program_add(request):
    if request.method == 'POST':
        form = SportProgramForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sport program added.')
            return redirect('manage:sport_programs_list')
    else:
        form = SportProgramForm(initial={'is_active': True})
    return render(request, 'pages/manage/sport_program_form.html', {'form': form, 'title': 'Add sport program'})


@require_admin
def sport_program_edit(request, pk):
    obj = get_object_or_404(SportProgram, pk=pk)
    if request.method == 'POST':
        form = SportProgramForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sport program updated.')
            return redirect('manage:sport_programs_list')
    else:
        form = SportProgramForm(instance=obj)
    return render(request, 'pages/manage/sport_program_form.html', {'form': form, 'title': 'Edit sport program', 'item': obj})


@require_admin
def sport_program_delete(request, pk):
    obj = get_object_or_404(SportProgram, pk=pk)
    if request.method == 'POST':
        name = obj.name
        obj.delete()
        messages.success(request, f'"{name}" deleted.')
        return redirect('manage:sport_programs_list')
    return render(request, 'pages/manage/confirm_delete.html', {'item': obj, 'cancel_url': 'manage:sport_programs_list', 'label': 'sport program'})


@require_admin
def teams_list(request):
    items = Team.objects.all().select_related('sport_program').order_by('sport_program', 'name')
    return render(request, 'pages/manage/teams_list.html', {'items': items})


@require_admin
def team_add(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team added.')
            return redirect('manage:teams_list')
    else:
        form = TeamForm(initial={'is_active': True})
    return render(request, 'pages/manage/team_form.html', {'form': form, 'title': 'Add team'})


@require_admin
def team_edit(request, pk):
    obj = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Team updated.')
            return redirect('manage:teams_list')
    else:
        form = TeamForm(instance=obj)
    return render(request, 'pages/manage/team_form.html', {'form': form, 'title': 'Edit team', 'item': obj})


@require_admin
def team_delete(request, pk):
    obj = get_object_or_404(Team, pk=pk)
    if request.method == 'POST':
        name = obj.name
        obj.delete()
        messages.success(request, f'"{name}" deleted.')
        return redirect('manage:teams_list')
    return render(request, 'pages/manage/confirm_delete.html', {'item': obj, 'cancel_url': 'manage:teams_list', 'label': 'team'})


# ---------- About page ----------
@require_admin
def about_edit(request):
    obj = AboutPage.load()
    if request.method == 'POST':
        form = AboutPageForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'About page content saved.')
            return redirect('manage:about_edit')
    else:
        form = AboutPageForm(instance=obj)
    return render(request, 'pages/manage/about_edit.html', {'form': form})


# ---------- Officials ----------
@require_admin
def officials_list(request):
    items = Official.objects.all().order_by('order', 'name')
    return render(request, 'pages/manage/officials_list.html', {'items': items})


@require_admin
def official_add(request):
    if request.method == 'POST':
        form = OfficialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Official added.')
            return redirect('manage:officials_list')
    else:
        form = OfficialForm(initial={'is_published': True, 'order': 0})
    return render(request, 'pages/manage/official_form.html', {'form': form, 'title': 'Add official'})


@require_admin
def official_edit(request, pk):
    obj = get_object_or_404(Official, pk=pk)
    if request.method == 'POST':
        form = OfficialForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Official updated.')
            return redirect('manage:officials_list')
    else:
        form = OfficialForm(instance=obj)
    return render(request, 'pages/manage/official_form.html', {'form': form, 'title': 'Edit official', 'item': obj})


@require_admin
def official_delete(request, pk):
    obj = get_object_or_404(Official, pk=pk)
    if request.method == 'POST':
        name = obj.name
        obj.delete()
        messages.success(request, f'"{name}" deleted.')
        return redirect('manage:officials_list')
    return render(request, 'pages/manage/confirm_delete.html', {'item': obj, 'cancel_url': 'manage:officials_list', 'label': 'official'})


# ---------- Youth jobs ----------
@require_admin
def youth_jobs_list(request):
    items = YouthJob.objects.all().order_by('-created_at')[:80]
    return render(request, 'pages/manage/youth_jobs_list.html', {'items': items})


@require_admin
def youth_job_add(request):
    if request.method == 'POST':
        form = YouthJobForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Youth job / opportunity added.')
            return redirect('manage:youth_jobs_list')
    else:
        form = YouthJobForm(initial={'is_published': True})
    return render(request, 'pages/manage/youth_job_form.html', {'form': form, 'title': 'Add opportunity'})


@require_admin
def youth_job_edit(request, pk):
    obj = get_object_or_404(YouthJob, pk=pk)
    if request.method == 'POST':
        form = YouthJobForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Opportunity updated.')
            return redirect('manage:youth_jobs_list')
    else:
        form = YouthJobForm(instance=obj)
    return render(request, 'pages/manage/youth_job_form.html', {'form': form, 'title': 'Edit opportunity', 'item': obj})


@require_admin
def youth_job_delete(request, pk):
    obj = get_object_or_404(YouthJob, pk=pk)
    if request.method == 'POST':
        title = obj.title
        obj.delete()
        messages.success(request, f'"{title}" deleted.')
        return redirect('manage:youth_jobs_list')
    return render(request, 'pages/manage/confirm_delete.html', {'item': obj, 'cancel_url': 'manage:youth_jobs_list', 'label': 'opportunity'})


# ---------- Section backgrounds ----------
@require_admin
def section_styles_list(request):
    items = SectionStyle.objects.all().prefetch_related('slides').order_by('section_key')
    return render(request, 'pages/manage/section_styles_list.html', {'items': items})


@require_admin
def section_style_add(request):
    if request.method == 'POST':
        form = SectionStyleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Section background added.')
            return redirect('manage:section_styles_list')
    else:
        form = SectionStyleForm(initial={'is_active': True, 'background_type': 'plain', 'background_color': '#ffffff', 'slide_interval_seconds': 5})
    return render(request, 'pages/manage/section_style_form.html', {'form': form, 'title': 'Add section background'})


@require_admin
def section_style_edit(request, pk):
    obj = get_object_or_404(SectionStyle, pk=pk)
    if request.method == 'POST':
        form = SectionStyleForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Section background updated.')
            return redirect('manage:section_styles_list')
    else:
        form = SectionStyleForm(instance=obj)
    slide_form = SectionSlideForm(initial={'section_style': obj, 'order': obj.slides.count()})
    return render(request, 'pages/manage/section_style_form.html', {
        'form': form, 'title': 'Edit section background', 'item': obj,
        'slide_form': slide_form,
    })


@require_admin
def section_style_delete(request, pk):
    obj = get_object_or_404(SectionStyle, pk=pk)
    if request.method == 'POST':
        key = obj.section_key
        obj.delete()
        messages.success(request, f'Section "{key}" deleted.')
        return redirect('manage:section_styles_list')
    return render(request, 'pages/manage/confirm_delete.html', {'item': obj, 'cancel_url': 'manage:section_styles_list', 'label': 'section background'})


@require_admin
def section_slide_add(request, section_pk):
    section_style = get_object_or_404(SectionStyle, pk=section_pk)
    if request.method == 'POST':
        form = SectionSlideForm(request.POST, request.FILES)
        if form.is_valid():
            slide = form.save(commit=False)
            slide.section_style = section_style
            slide.save()
            messages.success(request, 'Slide added.')
            return redirect('manage:section_style_edit', pk=section_pk)
    else:
        form = SectionSlideForm(initial={'order': section_style.slides.count()})
    return render(request, 'pages/manage/section_slide_form.html', {'form': form, 'section_style': section_style})


@require_admin
def section_slide_delete(request, pk):
    slide = get_object_or_404(SectionSlide, pk=pk)
    section_pk = slide.section_style_id
    if request.method == 'POST':
        slide.delete()
        messages.success(request, 'Slide removed.')
        return redirect('manage:section_style_edit', pk=section_pk)
    cancel_link = reverse('manage:section_style_edit', kwargs={'pk': section_pk})
    return render(request, 'pages/manage/confirm_delete.html', {'item': slide, 'cancel_url': 'manage:section_styles_list', 'cancel_link': cancel_link, 'label': 'slide'})
