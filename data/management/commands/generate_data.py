import random
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from faker import Faker
from tqdm import tqdm

from data.models import DataCollection
from project.models import ResearchProject
from users.models import Participant, Profile


class Command(BaseCommand):
    help = "Generate dummy data for testing"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Generate 100 users with profiles
        self.stdout.write("Generating 100 users...")
        users = []
        for i in tqdm(range(100), desc="Users"):
            username = fake.user_name()
            email = fake.email()
            user = User(username=username + str(i), email=email)
            user.set_password("password")
            users.append(user)
        users = User.objects.bulk_create(users)
        self.stdout.write("100 users created.")

        # Create profiles for the users
        self.stdout.write("Generating profiles for users...")  # Refresh the user list after bulk creation
        profiles = [
            Profile(user=user) for user in tqdm(users, desc="Profiles")
        ]
        Profile.objects.bulk_create(profiles)
        self.stdout.write("Profiles created.")

        # Generate 50 research projects
        self.stdout.write("Generating 50 research projects...")
        research_projects = []
        for _ in tqdm(range(50), desc="Research Projects"):
            title = fake.catch_phrase()
            description = fake.text(max_nb_chars=200)
            start_date = now() - timedelta(days=random.randint(30, 365))
            end_date = start_date + timedelta(days=random.randint(30, 365))
            created_by = random.choice(users)
            project = ResearchProject(
                title=title,
                description=description,
                start_date=start_date,
                end_date=end_date,
                created_by=created_by,
            )
            research_projects.append(project)
        ResearchProject.objects.bulk_create(research_projects)
        self.stdout.write("50 research projects created.")

        # Generate 100 data collections
        self.stdout.write("Generating 100 data collections...")
        profiles = list(Profile.objects.all())  # Ensure we fetch updated profiles
        research_projects = list(ResearchProject.objects.all())
        data_collections = []
        for _ in tqdm(range(100), desc="Data Collections"):
            participant = random.choice(list(Participant.objects.all()))
            project = random.choice(research_projects)
            submission_date = now() - timedelta(days=random.randint(1, 180))
            data_file = f"media/media/Year_3B_TERM_I_2024-2025.xlsx"
            data_collection = DataCollection(
                participant=participant,
                project=project,
                data_submission_date=submission_date,
                data=data_file,
            )
            data_collections.append(data_collection)
        DataCollection.objects.bulk_create(data_collections)
        self.stdout.write("100 data collections created.")

        self.stdout.write("Data generation complete.")
