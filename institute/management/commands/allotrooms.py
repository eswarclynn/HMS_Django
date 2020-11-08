import os, csv, traceback
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from institute.models import Block, Student
from django.conf import settings


class Command(BaseCommand):
    help = "Imports Students from given CSV file to Student Model."

    def get_file_path(self, file_name):
        return os.path.join(settings.BASE_DIR, "data", file_name)

    def get_floor_from_letter(self, letter):
        if letter == "G":
            return "Ground"
        elif letter == "F":
            return "First"
        elif letter == "S":
            return "Second"
        else:
            raise ValidationError("Only Ground(G), First(F) and Second(S) floors accepted!")


    def add_arguments(self, parser):
        parser.add_argument("file_name", nargs="+", type=str)

    def handle(self, *args, **options):
        file_path = self.get_file_path(options["file_name"][0])
        try:
            with open(file_path) as csv_file:
                csv_reader = csv.DictReader(csv_file, delimiter=",")
                self.stdout.write(self.style.SUCCESS("Reading: {}".format(file_path)))
                
                created, rejected = [0, 0]
                for data in csv_reader:
                    try:
                        student = Student.objects.get(roll_no = data["id"])
                        roomdetail = student.roomdetail
                        roomdetail.room_no = int(data["Room no"])
                        roomdetail.floor = self.get_floor_from_letter(data["floor"])
                        roomdetail.block = (Block.objects.filter(name__contains = data["block name"]) | Block.objects.filter(name__contains = data["block name"].capitalize())).first()
                        roomdetail.full_clean()
                        roomdetail.save()
                        created += 1

                    except Student.DoesNotExist:
                        print("Invalid Student ID: {}".format(data["id"]))
                        rejected += 1 
                    except Exception as e:
                        if data["id"]:
                            print("Error while inserting student - {}: {}".format(data["id"], e.messages))
                            # traceback.print_exc()
                        else:
                            pass
                        rejected += 1 

        except Exception as e:
            raise CommandError("Error: {}".format(e))

        self.stdout.write(self.style.SUCCESS('Successfully imported {} students. Rejected {} students.'.format(created, rejected)))