# Data migration: seed Kiambu County constituencies and wards for registration dropdowns

from django.db import migrations


def seed_constituencies_wards(apps, schema_editor):
    Constituency = apps.get_model('core', 'Constituency')
    Ward = apps.get_model('core', 'Ward')
    # Kiambu County: 12 constituencies and their wards (IEBC)
    data = [
        (1, 'Gatundu North', ['Gituamba', 'Githobokoni', 'Chania', "Mang'u"]),
        (2, 'Gatundu South', ['Kiamwangi', 'Kiganjo', 'Ndarugo', 'Ngenda']),
        (3, 'Githunguri', ['Githunguri', 'Githiga', 'Ikinu', 'Ngewa', 'Komothai']),
        (4, 'Juja', ['Murera', 'Theta', 'Juja', 'Witeithie', 'Kalimoni']),
        (5, 'Kabete', ['Gitaru', 'Muguga', 'Nyathuna', 'Kabete', 'Uthiru']),
        (6, 'Kiambaa', ['Cianda', 'Karuri', 'Ndenderu', 'Muchatha', 'Kihara']),
        (7, 'Kiambu', ["Ting'ang'a", 'Ndumberi', 'Riabai', 'Township']),
        (8, 'Kikuyu', ['Karai', 'Nachu', 'Sigona', 'Kikuyu', 'Kinoo']),
        (9, 'Lari', ['Kinale', 'Kijabe', 'Nyanduma', 'Kamburu', 'Lari/Kirenga']),
        (10, 'Limuru', ['Bibirioni', 'Limuru Central', 'Ndeiya', 'Limuru East', 'Ngecha/Tigoni']),
        (11, 'Ruiru', ['Gitothua', 'Biashara', 'Gatongora', 'Kahawa/Sukari', 'Kahawa Wendani', 'Kiuu', 'Mwiki', 'Mwihoko']),
        (12, 'Thika Town', ['Township', 'Kamenu', 'Hospital', 'Gatuanyaga', 'Ngoliba']),
    ]
    for order, name, ward_names in data:
        c, _ = Constituency.objects.get_or_create(name=name, defaults={'order': order})
        for i, wname in enumerate(ward_names):
            Ward.objects.get_or_create(constituency=c, name=wname, defaults={'order': i + 1})


def reverse_seed(apps, schema_editor):
    Ward = apps.get_model('core', 'Ward')
    Constituency = apps.get_model('core', 'Constituency')
    User = apps.get_model('core', 'User')
    User.objects.filter(ward__isnull=False).update(ward=None)
    Ward.objects.all().delete()
    Constituency.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_donor_county_official_roles'),
    ]

    operations = [
        migrations.RunPython(seed_constituencies_wards, reverse_seed),
    ]
