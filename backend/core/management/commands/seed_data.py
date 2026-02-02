from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from projects.models import County, Ministry, ProjectCategory, Project
from funding.models import FundingSource, Sponsor
from events.models import Event, Announcement
from sports.models import SportProgram
from gamification.models import Badge

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed initial data for AGCBO'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # Create superuser if doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@agcbo.org',
                password='admin123',
                role='super_admin',
                is_approved=True,
                is_verified=True
            )
            self.stdout.write(self.style.SUCCESS('Created superuser: admin/admin123'))

        # Create Counties
        counties_data = [
            {'name': 'Kiambu', 'code': '001'},
            {'name': 'Nairobi', 'code': '002'},
            {'name': 'Nakuru', 'code': '003'},
        ]
        for county_data in counties_data:
            County.objects.get_or_create(name=county_data['name'], defaults=county_data)
        self.stdout.write(self.style.SUCCESS('Created counties'))

        # Create Ministries
        ministries_data = [
            {'name': 'Ministry of Youth Affairs', 'abbreviation': 'MOYA'},
            {'name': 'Ministry of Agriculture', 'abbreviation': 'MOA'},
            {'name': 'Ministry of Sports', 'abbreviation': 'MOS'},
            {'name': 'Ministry of Environment', 'abbreviation': 'MOE'},
        ]
        for ministry_data in ministries_data:
            Ministry.objects.get_or_create(name=ministry_data['name'], defaults=ministry_data)
        self.stdout.write(self.style.SUCCESS('Created ministries'))

        # Create Project Categories
        categories_data = [
            {'name': 'Youth Empowerment', 'slug': 'youth-empowerment', 'icon': 'fa-users', 'color': '#0d4f3c'},
            {'name': 'Agriculture', 'slug': 'agriculture', 'icon': 'fa-seedling', 'color': '#14b8a6'},
            {'name': 'Environment', 'slug': 'environment', 'icon': 'fa-leaf', 'color': '#0ea5e9'},
            {'name': 'Education', 'slug': 'education', 'icon': 'fa-graduation-cap', 'color': '#fbbf24'},
            {'name': 'Health', 'slug': 'health', 'icon': 'fa-heart', 'color': '#dc2626'},
        ]
        for cat_data in categories_data:
            ProjectCategory.objects.get_or_create(slug=cat_data['slug'], defaults=cat_data)
        self.stdout.write(self.style.SUCCESS('Created project categories'))

        # Create Funding Sources
        kiambu = County.objects.get(name='Kiambu')
        funding_sources_data = [
            {'name': 'Kiambu County Government', 'source_type': 'county', 'county': kiambu},
            {'name': 'Ministry of Youth Affairs', 'source_type': 'ministry'},
        ]
        for fs_data in funding_sources_data:
            FundingSource.objects.get_or_create(name=fs_data['name'], defaults=fs_data)
        self.stdout.write(self.style.SUCCESS('Created funding sources'))

        # Create Sponsors
        sponsors_data = [
            {'name': 'Local Business Partner 1', 'organization_type': 'Private Sector'},
            {'name': 'Community Foundation', 'organization_type': 'NGO'},
        ]
        for sponsor_data in sponsors_data:
            Sponsor.objects.get_or_create(name=sponsor_data['name'], defaults=sponsor_data)
        self.stdout.write(self.style.SUCCESS('Created sponsors'))

        # Create Badges
        badges_data = [
            {'name': 'Active Youth', 'slug': 'active-youth', 'description': 'For active participation', 'points_required': 100, 'badge_type': 'participation'},
            {'name': 'Volunteer Champion', 'slug': 'volunteer-champion', 'description': 'For outstanding volunteer work', 'points_required': 500, 'badge_type': 'volunteer'},
            {'name': 'Project Leader', 'slug': 'project-leader', 'description': 'For leading a project', 'points_required': 1000, 'badge_type': 'leadership'},
        ]
        for badge_data in badges_data:
            Badge.objects.get_or_create(slug=badge_data['slug'], defaults=badge_data)
        self.stdout.write(self.style.SUCCESS('Created badges'))

        # Create Sport Programs
        sports_data = [
            {'name': 'Football', 'sport_type': 'Football'},
            {'name': 'Basketball', 'sport_type': 'Basketball'},
            {'name': 'Athletics', 'sport_type': 'Athletics'},
        ]
        for sport_data in sports_data:
            SportProgram.objects.get_or_create(name=sport_data['name'], defaults=sport_data)
        self.stdout.write(self.style.SUCCESS('Created sport programs'))

        # Create Sample Announcement
        admin_user = User.objects.get(username='admin')
        Announcement.objects.get_or_create(
            title='Welcome to AGCBO Digital Hub',
            defaults={
                'slug': 'welcome-to-agcbo-digital-hub',
                'content': 'Welcome to the AGCBO Digital Hub! We are excited to have you here.',
                'is_published': True,
                'is_featured': True,
                'created_by': admin_user,
            }
        )
        self.stdout.write(self.style.SUCCESS('Created sample announcement'))

        self.stdout.write(self.style.SUCCESS('\n✅ Data seeding completed!'))
