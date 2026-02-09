from django import forms
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from core.models import Constituency, Ward, SiteSettings, Official, YouthJob, AboutPage, SectionStyle, SectionSlide
from gallery.models import GalleryItem
from projects.models import Project, ProjectCategory, County, Ministry
from events.models import Event
from sports.models import SportProgram, Team

User = get_user_model()


class SectionStyleForm(forms.ModelForm):
    class Meta:
        model = SectionStyle
        fields = [
            'section_key', 'label', 'background_type', 'background_color',
            'background_image', 'background_video', 'background_video_url',
            'slide_interval_seconds', 'is_active'
        ]
        widgets = {
            'section_key': forms.TextInput(attrs={'class': 'input', 'placeholder': 'e.g. header, hero, footer'}),
            'label': forms.TextInput(attrs={'class': 'input'}),
            'background_color': forms.TextInput(attrs={'class': 'input', 'placeholder': '#ffffff'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name not in self.Meta.widgets and hasattr(field, 'widget') and not isinstance(field.widget, (forms.Textarea, forms.CheckboxInput)):
                field.widget.attrs.setdefault('class', 'input')


class SectionSlideForm(forms.ModelForm):
    class Meta:
        model = SectionSlide
        fields = ['image', 'order', 'caption']
        widgets = {
            'order': forms.NumberInput(attrs={'class': 'input', 'min': 0}),
            'caption': forms.TextInput(attrs={'class': 'input'}),
        }


class SiteSettingsForm(forms.ModelForm):
    """Form for editing site settings in the custom manage area."""
    class Meta:
        model = SiteSettings
        fields = [
            'site_name', 'registration_number', 'logo', 'favicon',
            'hotline_1', 'hotline_2', 'hotline_3', 'email', 'address', 'box_number',
            'facebook_url', 'twitter_url', 'instagram_url', 'youtube_url', 'linkedin_url',
        ]
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'site_name': forms.TextInput(attrs={'class': 'input'}),
            'registration_number': forms.TextInput(attrs={'class': 'input'}),
            'email': forms.EmailInput(attrs={'class': 'input'}),
            'address': forms.Textarea(attrs={'class': 'input', 'rows': 3}),
            'box_number': forms.TextInput(attrs={'class': 'input'}),
            'hotline_1': forms.TextInput(attrs={'class': 'input'}),
            'hotline_2': forms.TextInput(attrs={'class': 'input'}),
            'hotline_3': forms.TextInput(attrs={'class': 'input'}),
            'facebook_url': forms.URLInput(attrs={'class': 'input'}),
            'twitter_url': forms.URLInput(attrs={'class': 'input'}),
            'instagram_url': forms.URLInput(attrs={'class': 'input'}),
            'youtube_url': forms.URLInput(attrs={'class': 'input'}),
            'linkedin_url': forms.URLInput(attrs={'class': 'input'}),
        }


class GalleryItemForm(forms.ModelForm):
    """Form for adding/editing gallery items (image or video link)."""
    class Meta:
        model = GalleryItem
        fields = ['title', 'description', 'media_type', 'file', 'url', 'year', 'tags', 'is_featured', 'is_public']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input', 'placeholder': 'e.g. Community meeting 2024'}),
            'description': forms.Textarea(attrs={'class': 'input', 'rows': 2, 'placeholder': 'Optional description'}),
            'media_type': forms.Select(attrs={'class': 'input'}),
            'year': forms.NumberInput(attrs={'class': 'input', 'min': 2000, 'max': 2030}),
            'tags': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Comma-separated tags'}),
            'url': forms.URLInput(attrs={'class': 'input', 'placeholder': 'Image URL or YouTube/Vimeo link for videos'}),
        }

    def clean(self):
        data = super().clean()
        if not data.get('file') and not data.get('url'):
            raise forms.ValidationError('Provide either an uploaded file or a link (URL).')
        return data


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'title', 'slug', 'description', 'objectives', 'category', 'county', 'ministry', 'status',
            'featured_image', 'budget_amount', 'budget_currency', 'allocated_amount', 'spent_amount',
            'start_date', 'end_date', 'completion_date', 'is_featured', 'is_public'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input'}),
            'slug': forms.TextInput(attrs={'class': 'input'}),
            'description': forms.Textarea(attrs={'class': 'input', 'rows': 4}),
            'objectives': forms.Textarea(attrs={'class': 'input', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name not in self.Meta.widgets and hasattr(field, 'widget') and not isinstance(field.widget, (forms.Textarea, forms.SelectMultiple, forms.CheckboxInput)):
                field.widget.attrs.setdefault('class', 'input')


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'slug', 'description', 'event_type', 'featured_image',
            'venue', 'county', 'address', 'is_online', 'online_link',
            'start_date', 'end_date', 'registration_deadline',
            'requires_registration', 'max_participants', 'registration_fee',
            'project', 'is_published', 'is_featured'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'class': 'input', 'rows': 4}),
            'address': forms.Textarea(attrs={'class': 'input', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name not in ('description', 'address') and hasattr(field, 'widget') and not isinstance(field.widget, (forms.Textarea, forms.SelectMultiple, forms.CheckboxInput)):
                field.widget.attrs.setdefault('class', 'input')


class SportProgramForm(forms.ModelForm):
    class Meta:
        model = SportProgram
        fields = ['name', 'description', 'sport_type', 'logo', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'input', 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'description' and hasattr(field, 'widget') and not isinstance(field.widget, (forms.Textarea, forms.CheckboxInput)):
                field.widget.attrs.setdefault('class', 'input')


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'sport_program', 'description', 'logo', 'coach_name', 'coach_phone', 'is_active']
        widgets = {'description': forms.Textarea(attrs={'class': 'input', 'rows': 2})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'description' and hasattr(field, 'widget') and not isinstance(field.widget, (forms.Textarea, forms.CheckboxInput)):
                field.widget.attrs.setdefault('class', 'input')


class AboutPageForm(forms.ModelForm):
    class Meta:
        model = AboutPage
        fields = ['tagline', 'vision', 'mission', 'our_story']
        widgets = {
            'tagline': forms.TextInput(attrs={'class': 'input'}),
            'vision': forms.Textarea(attrs={'class': 'input', 'rows': 4}),
            'mission': forms.Textarea(attrs={'class': 'input', 'rows': 4}),
            'our_story': forms.Textarea(attrs={'class': 'input', 'rows': 6}),
        }


class OfficialForm(forms.ModelForm):
    class Meta:
        model = Official
        fields = ['name', 'title', 'bio', 'photo', 'email', 'phone', 'order', 'is_published']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'input', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'bio' and hasattr(field, 'widget') and not isinstance(field.widget, (forms.Textarea, forms.CheckboxInput)):
                field.widget.attrs.setdefault('class', 'input')


class YouthJobForm(forms.ModelForm):
    class Meta:
        model = YouthJob
        fields = [
            'title', 'description', 'organization', 'location',
            'application_deadline', 'apply_url', 'contact_email', 'contact_phone', 'is_published'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'class': 'input', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'description' and hasattr(field, 'widget') and not isinstance(field.widget, (forms.Textarea, forms.CheckboxInput)):
                field.widget.attrs.setdefault('class', 'input')


class UserCreateForm(forms.ModelForm):
    """Add user from manage dashboard. Only super_admin can create admin/super_admin users."""
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}), min_length=8, label='Password', required=False)
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}), min_length=8, label='Confirm password', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'ward', 'role', 'is_approved', 'is_active']
        widgets = {f: forms.TextInput(attrs={'class': 'input'}) for f in ['username', 'email', 'first_name', 'last_name', 'phone_number']}
        widgets['role'] = forms.Select(attrs={'class': 'input'})
        widgets['ward'] = forms.Select(attrs={'class': 'input'})

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['ward'].queryset = Ward.objects.all().order_by('constituency', 'name')
        self.fields['ward'].required = False
        if self.instance and self.instance.pk:
            self.fields['password'].required = False
            self.fields['password_confirm'].required = False
        if self.request and getattr(self.request.user, 'role', None) != 'super_admin':
            self.fields['role'].choices = [c for c in User.ROLE_CHOICES if c[0] not in ('admin', 'super_admin')]

    def clean(self):
        data = super().clean()
        if not self.instance.pk:
            if not data.get('password'):
                raise forms.ValidationError('Password is required for new users.')
            if data.get('password') != data.get('password_confirm'):
                raise forms.ValidationError('Passwords do not match.')
        elif data.get('password') and data.get('password') != data.get('password_confirm'):
            raise forms.ValidationError('Passwords do not match.')
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    """Edit user role, approval, active status. Only super_admin can set role to admin/super_admin."""
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'ward', 'role', 'is_approved', 'is_verified', 'is_active']
        widgets = {f: forms.TextInput(attrs={'class': 'input'}) for f in ['username', 'email', 'first_name', 'last_name', 'phone_number']}
        widgets['role'] = forms.Select(attrs={'class': 'input'})
        widgets['ward'] = forms.Select(attrs={'class': 'input'})

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['ward'].queryset = Ward.objects.all().order_by('constituency', 'name')
        if self.request and getattr(self.request.user, 'role', None) != 'super_admin':
            self.fields['role'].choices = [c for c in User.ROLE_CHOICES if c[0] not in ('admin', 'super_admin')]


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, label='Password')
    password_confirm = forms.CharField(widget=forms.PasswordInput, min_length=8, label='Confirm Password')
    # Required for CBO membership (as on Government ID/Passport)
    id_or_passport_number = forms.CharField(max_length=30, required=True, label='ID or Passport number')
    full_names_as_on_id = forms.CharField(max_length=200, required=True, label='Full names as on ID/Passport')
    constituency = forms.ModelChoiceField(queryset=Constituency.objects.all(), required=True, empty_label='Select constituency')
    ward = forms.ModelChoiceField(queryset=Ward.objects.none(), required=True, empty_label='Select ward (choose constituency first)')
    phone_number = forms.CharField(max_length=20, required=True, label='Phone number')
    email = forms.EmailField(required=False, label='Email (optional)')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'id_or_passport_number', 'full_names_as_on_id', 'ward']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = False
        if self.data and 'constituency' in self.data:
            try:
                cid = int(self.data.get('constituency'))
                self.fields['ward'].queryset = Ward.objects.filter(constituency_id=cid).order_by('name')
            except (ValueError, TypeError):
                self.fields['ward'].queryset = Ward.objects.none()
        elif self.instance and self.instance.pk and getattr(self.instance, 'ward_id', None):
            self.fields['ward'].queryset = Ward.objects.filter(constituency=self.instance.ward.constituency).order_by('name')
        else:
            self.fields['ward'].queryset = Ward.objects.none()

    def clean_ward(self):
        ward = self.cleaned_data.get('ward')
        constituency = self.cleaned_data.get('constituency')
        if ward and constituency and ward.constituency_id != constituency.id:
            raise forms.ValidationError('Ward must belong to the selected constituency.')
        return ward

    def clean(self):
        data = super().clean()
        if data.get('password') != data.get('password_confirm'):
            raise forms.ValidationError('Passwords do not match')
        return data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = 'member'
        user.is_approved = False
        user.id_or_passport_number = self.cleaned_data.get('id_or_passport_number')
        user.full_names_as_on_id = self.cleaned_data.get('full_names_as_on_id')
        if commit:
            user.save()
        return user


class DonorRegisterForm(forms.Form):
    """Donor/Sponsor registration: name or company, email, phone, credentials."""
    name_or_company = forms.CharField(max_length=200, required=True, label='Name or Company name')
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, label='Password')
    password_confirm = forms.CharField(widget=forms.PasswordInput, min_length=8, label='Confirm password')

    def clean_username(self):
        from django.contrib.auth import get_user_model
        if get_user_model().objects.filter(username=self.cleaned_data['username'].strip()).exists():
            raise forms.ValidationError('This username is already taken.')
        return self.cleaned_data['username'].strip()

    def clean(self):
        data = super().clean()
        if data.get('password') != data.get('password_confirm'):
            raise forms.ValidationError('Passwords do not match.')
        return data

    def save(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['name_or_company'][:30],
            phone_number=self.cleaned_data['phone'],
            role='donor',
            is_approved=False,
            is_staff=False,
            is_superuser=False,
        )
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


class CountyOfficialRegisterForm(forms.Form):
    """County official registration: name, department, phone, email, password."""
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    department = forms.ChoiceField(choices=User.DEPARTMENT_CHOICES, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, label='Password')
    password_confirm = forms.CharField(widget=forms.PasswordInput, min_length=8, label='Confirm password')

    def clean_username(self):
        from django.contrib.auth import get_user_model
        if get_user_model().objects.filter(username=self.cleaned_data['username'].strip()).exists():
            raise forms.ValidationError('This username is already taken.')
        return self.cleaned_data['username'].strip()

    def clean(self):
        data = super().clean()
        if data.get('password') != data.get('password_confirm'):
            raise forms.ValidationError('Passwords do not match.')
        return data

    def save(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        user = User(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            phone_number=self.cleaned_data['phone_number'],
            department=self.cleaned_data['department'],
            role='county_official',
            is_verified=False,
            is_staff=False,
            is_superuser=False,
        )
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user


class ContactForm(forms.Form):
    name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)
    subject = forms.CharField(max_length=200, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
