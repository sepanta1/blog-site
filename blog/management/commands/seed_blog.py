import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from blog.models import Category, Comment, Contact, Post


class Command(BaseCommand):
    help = "Seed blog app with dummy data using Faker"

    def add_arguments(self, parser):
        parser.add_argument("--posts", type=int, default=20)
        parser.add_argument("--comments", type=int, default=50)

    def handle(self, *args, **options):
        fake = Faker()
        posts_count = options["posts"]
        comments_count = options["comments"]

        self.stdout.write("🔄 Seeding data...")

        if not User.objects.exists():
            for _ in range(5):
                User.objects.create_user(
                    username=fake.user_name(),
                    email=fake.email(),
                    password="password123",
                )

        users = list(User.objects.all())

        categories = []
        for name in ["Django", "Python", "Web", "Backend", "Tutorial"]:
            category, _ = Category.objects.get_or_create(name=name)
            categories.append(category)

        posts = []
        for _ in range(posts_count):
            post = Post.objects.create(
                author=random.choice(users),
                title=fake.sentence(nb_words=6),
                content=f"<p>{fake.paragraph(nb_sentences=6)}</p>",
                counted_views=random.randint(0, 1000),
                status=random.choice([True, False]),
                published_date=timezone.now() if random.choice([True, False]) else None,
            )

            post.tags.add(*fake.words(nb=3))

            post.category.set(random.sample(categories, k=random.randint(1, 2)))

            posts.append(post)

        comments = []
        for _ in range(comments_count):
            post = random.choice(posts)

            comment = Comment.objects.create(
                parent_post=post,
                name=fake.name(),
                email=fake.email(),
                message=fake.sentence(),
                approved=random.choice([True, True, False]),
            )

            comments.append(comment)

        for _ in range(int(comments_count * 0.3)):
            parent = random.choice(comments)
            Comment.objects.create(
                parent_post=parent.parent_post,
                parent=parent,
                name=fake.name(),
                email=fake.email(),
                message=fake.sentence(),
                approved=True,
            )

        for _ in range(10):
            Contact.objects.create(
                name=fake.name(),
                email=fake.email(),
                subject=fake.sentence(),
                message=fake.paragraph(),
            )

        self.stdout.write(
            self.style.SUCCESS("✅ Blog dummy data created successfully!")
        )
