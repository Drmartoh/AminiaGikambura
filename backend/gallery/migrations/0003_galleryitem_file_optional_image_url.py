# Allow gallery image from URL (no file upload required)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='galleryitem',
            name='file',
            field=models.FileField(blank=True, help_text='Upload an image/video file', null=True, upload_to='gallery/'),
        ),
        migrations.AlterField(
            model_name='galleryitem',
            name='url',
            field=models.URLField(blank=True, help_text='Or paste a direct image/video URL (e.g. from Facebook, Instagram, or any website). Use either file upload OR link.'),
        ),
    ]
