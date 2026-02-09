"""
Seed Kiambu County constituencies and wards (from official administrative units).
Ref: https://kiambu.go.ke/administrative-units/
"""
from django.core.management.base import BaseCommand
from core.models import Constituency, Ward


KIAMBU_DATA = [
    ('Gatundu North', ['Gituamba', 'Githobokoni', 'Chania', "Mang'u"]),
    ('Gatundu South', ['Kiamwangi', 'Kiganjo', 'Ndarugo', 'Ngenda']),
    ('Githunguri', ['Githunguri', 'Githiga', 'Ikinu', 'Ngewa', 'Komothai']),
    ('Juja', ['Murera', 'Theta', 'Juja', 'Witeithie', 'Kalimoni']),
    ('Kabete', ['Gitaru', 'Muguga', 'Nyathuna', 'Kabete', 'Uthiru']),
    ('Kiambaa', ['Cianda', 'Karuri', 'Ndenderu', 'Muchatha', 'Kihara']),
    ('Kiambu', ["Ting'ang'a", 'Ndumberi', 'Riabai', 'Township']),
    ('Kikuyu', ['Karai', 'Nachu', 'Sigona', 'Kikuyu', 'Kinoo']),
    ('Lari', ['Kinale', 'Kijabe', 'Nyanduma', 'Kamburu', 'Lari/Kirenga']),
    ('Limuru', ['Bibirioni', 'Limuru Central', 'Ndeiya', 'Limuru East', 'Ngecha/Tigoni']),
    ('Ruiru', ['Gitothua', 'Biashara', 'Gatongora', 'Kahawa/Sukari', 'Kahawa Wendani', 'Kiuu', 'Mwiki', 'Mwihoko']),
    ('Thika Town', ['Township', 'Kamenu', 'Hospital', 'Gatuanyaga', 'Ngoliba']),
]


class Command(BaseCommand):
    help = 'Load Kiambu County constituencies and wards'

    def handle(self, *args, **options):
        for order, (const_name, ward_names) in enumerate(KIAMBU_DATA, 1):
            constituency, _ = Constituency.objects.get_or_create(
                name=const_name,
                defaults={'order': order}
            )
            for w_order, ward_name in enumerate(ward_names, 1):
                Ward.objects.get_or_create(
                    constituency=constituency,
                    name=ward_name,
                    defaults={'order': w_order}
                )
        self.stdout.write(self.style.SUCCESS(
            f'Seeded {Constituency.objects.count()} constituencies and {Ward.objects.count()} wards.'
        ))
