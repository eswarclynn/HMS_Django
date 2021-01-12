from django.core.management.base import BaseCommand, CommandError
from institute.models import Block
from django.conf import settings


class Command(BaseCommand):
    help = "Import Blocks to the system."

    BLOCKS = [
        {"name": "Godavari Hall of Residency",      "block_id": "4S-A", "gender": "Male", "room_type": "4S", "floor_count": 3, "capacity": 76},
        {"name": "Sabari Hall of Residency",        "block_id": "2S-A", "gender": "Male", "room_type": "2S", "floor_count": 3, "capacity": 100},
        {"name": "Indravathi Hall of Residency",    "block_id": "2S-B", "gender": "Male", "room_type": "2S", "floor_count": 3, "capacity": 100},
        {"name": "Pranahitha Hall of Residency",    "block_id": "2S-C", "gender": "Male", "room_type": "2S", "floor_count": 3, "capacity": 100},
        {"name": "Banganga Hall of Residency",      "block_id": "1S-A", "gender": "Male", "room_type": "1S", "floor_count": 3, "capacity": 100},
        {"name": "Purna Hall of Residency",         "block_id": "1S-B", "gender": "Male", "room_type": "1S", "floor_count": 3, "capacity": 100},
        {"name": "Manjeera Hall of Residency",      "block_id": "1S-C", "gender": "Male", "room_type": "1S", "floor_count": 3, "capacity": 100},
        
        {"name": "Krishnaveni Hall of Residency",   "block_id": "4S-FA", "gender": "Female", "room_type": "4S", "floor_count": 3, "capacity": 50},
        {"name": "Bheema Hall of Residency",        "block_id": "2S-FA", "gender": "Female", "room_type": "2S", "floor_count": 3, "capacity": 100},
        {"name": "Tungabhadra Hall of Residency",   "block_id": "2S-FB", "gender": "Female", "room_type": "2S", "floor_count": 3, "capacity": 100},
        {"name": "Ghataprabha Hall of Residency",   "block_id": "1S-FA", "gender": "Female", "room_type": "1S", "floor_count": 3, "capacity": 100},
        {"name": "Munneru Hall of Residency",       "block_id": "1S-FB", "gender": "Female", "room_type": "1S", "floor_count": 3, "capacity": 100},
        
        {"name": "4S-B Hall of Residency",          "block_id": "4S-B", "gender": "Male", "room_type": "4S", "floor_count": 5, "capacity": 115},
        {"name": "2S-D Hall of Residency",          "block_id": "2S-D", "gender": "Male", "room_type": "2S", "floor_count": 5, "capacity": 175},
        {"name": "1S-D Hall of Residency",          "block_id": "1S-D", "gender": "Male", "room_type": "1S", "floor_count": 5, "capacity": 175},
    ]


    def handle(self, *args, **options):
        try:
            for block_info in self.BLOCKS:
                block, created = Block.objects.get_or_create(**block_info)
                if created:
                    self.stdout.write(self.style.NOTICE("Created Block: {}.".format(block.name)))
        except Exception as e:
            raise CommandError("Error: {}".format(e))
        
        block_names = Block.objects.all().values_list('name', flat=True)
        self.stdout.write(self.style.SUCCESS('Available blocks: {}.'.format(", ".join(block_names))))