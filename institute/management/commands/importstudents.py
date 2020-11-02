import os, csv, traceback
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from institute.models import Student
from django.conf import settings


class Command(BaseCommand):
    help = "Imports Students from given CSV file to Student Model."

    def get_file_path(self, file_name):
        return os.path.join(settings.BASE_DIR, "data", file_name)

    def convert_date(self, date):
        month, day, year = list(map(lambda x: int(x), date.split("/")))
        return timezone.datetime(year=year, month=month, day=day)

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
                        # TODO: Modify Model to hold null data for blood group, community, 
                        # Required values for roll_no, year, branch, institute email, 
                        student = Student()
                        student.regd_no = data["StudentID"]
                        student.roll_no = data["roll_no"]
                        student.name = data["FullName"]
                        student.year = data["year"]
                        student.branch = data["branch"]
                        student.account_email = "{}@student.nitandhra.ac.in".format(student.roll_no)
                        student.email = data["StudentEmail"]
                        student.address = data["Address"]
                        student.phone = data["StudentMobile"]
                        student.parents_phone = data["ParentMobile"]
                        student.emergency_phone = data["ParentMobile"]
                        student.gender = data["Gender"]
                        student.community = data["Caste"]
                        student.dob = self.convert_date(data["BirthDate"])
                        student.blood_group = data["Bgroup"]
                        student.pwd = data["Disability"] == "1"
                        student.save()
                        created += 1

                    except Exception as e:
                        if data["StudentID"]:
                            print("Error while inserting student {} - {}".format(data["StudentID"], data["FullName"]))
                            traceback.print_exc()
                            print()
                        else:
                            pass
                        rejected += 1 

        except Exception as e:
            raise CommandError("Error: {}".format(e))

        self.stdout.write(self.style.SUCCESS('Successfully imported {} students. Rejected {} students.'.format(created, rejected)))