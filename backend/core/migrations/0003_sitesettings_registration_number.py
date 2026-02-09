# Generated manually - add CBO registration number to SiteSettings

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_constituency_ward_sitesettings_user_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='registration_number',
            field=models.CharField(blank=True, default='DSD/22/120/02/168788', help_text='CBO Registration No. (displayed in header and key areas)', max_length=80),
        ),
    ]
