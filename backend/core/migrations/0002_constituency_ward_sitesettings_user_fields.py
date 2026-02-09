# Generated manually for Constituency, Ward, SiteSettings and User fields

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('order', models.PositiveSmallIntegerField(default=0, help_text='Display order')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Constituencies',
                'ordering': ['order', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Ward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('order', models.PositiveSmallIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('constituency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wards', to='core.constituency')),
            ],
            options={
                'verbose_name_plural': 'Wards',
                'ordering': ['constituency', 'order', 'name'],
                'unique_together': {('constituency', 'name')},
            },
        ),
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default='AGCBO Digital Hub', max_length=200)),
                ('logo', models.ImageField(blank=True, help_text='Organization logo (header)', null=True, upload_to='site/')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='site/')),
                ('hotline_1', models.CharField(blank=True, default='+254715574285', max_length=25)),
                ('hotline_2', models.CharField(blank=True, max_length=25)),
                ('hotline_3', models.CharField(blank=True, max_length=25)),
                ('email', models.EmailField(blank=True, default='info@agcbo.org', max_length=254)),
                ('address', models.TextField(blank=True, default="Gikambura (BUJU), Karai Ward Labour Office, Just Besides MCA's Office Along Gikambura Stadium")),
                ('box_number', models.CharField(blank=True, max_length=50)),
                ('facebook_url', models.URLField(blank=True)),
                ('twitter_url', models.URLField(blank=True)),
                ('instagram_url', models.URLField(blank=True)),
                ('youtube_url', models.URLField(blank=True)),
                ('linkedin_url', models.URLField(blank=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Site settings',
                'verbose_name_plural': 'Site settings',
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='id_or_passport_number',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='ID or Passport number'),
        ),
        migrations.AddField(
            model_name='user',
            name='full_names_as_on_id',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Full names as on ID/Passport'),
        ),
        migrations.AddField(
            model_name='user',
            name='ward',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='core.ward'),
        ),
    ]
