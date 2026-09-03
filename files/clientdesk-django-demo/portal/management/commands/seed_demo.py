from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from portal.models import Client, Project, ProjectUpdate


class Command(BaseCommand):
    help = "Seed demo data for ClientDesk"

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@neoux.demo", "clientdesk2026")
            self.stdout.write(self.style.SUCCESS("Created admin superuser (admin / clientdesk2026)"))

        if not User.objects.filter(username="client1").exists():
            user = User.objects.create_user("client1", "client1@neoux.demo", "clientdesk2026")
            client = Client.objects.create(user=user, company_name="Anand Textiles Pvt Ltd", phone="+91 98765 43210")

            p1 = Project.objects.create(
                client=client,
                title="Company website rebuild",
                description="Full rebuild of the corporate site with a new product catalogue, enquiry form and mobile-first layout.",
                status="in_progress",
                progress_percent=65,
            )
            ProjectUpdate.objects.create(project=p1, note="Homepage and product pages approved. Moving to contact form + hosting setup this week.")
            ProjectUpdate.objects.create(project=p1, note="Initial design review completed. Two rounds of feedback incorporated.")

            p2 = Project.objects.create(
                client=client,
                title="CNC seal audit — Line 2",
                description="On-site inspection and re-specification of hydraulic seals for Line 2 CNC machines.",
                status="review",
                progress_percent=85,
            )
            ProjectUpdate.objects.create(project=p2, note="Draft diagnostic report shared for client review.")

            self.stdout.write(self.style.SUCCESS("Created demo client (client1 / clientdesk2026) with 2 projects"))
        else:
            self.stdout.write("Demo data already present.")
