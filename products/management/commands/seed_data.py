from django.core.management.base import BaseCommand
from faker import Faker
import random
from products.models import Category, Product
from stores.models import Store, Inventory

class Command(BaseCommand):
    help = "Seed the database with dummy data"

    def handle(self, *args, **options):
        fake = Faker()

        # --- Categories ---
        categories = []
        for _ in range(10):
            cat = Category.objects.create(name=fake.word().capitalize())
            categories.append(cat)
        self.stdout.write(self.style.SUCCESS("10+ Categories created."))

        # --- Products ---
        products = []
        for _ in range(1000):
            prod = Product.objects.create(
                title=fake.word().capitalize(),
                description=fake.sentence(),
                price=random.randint(100, 100000),
                category=random.choice(categories)
            )
            products.append(prod)
        self.stdout.write(self.style.SUCCESS("1000+ Products created."))

        # --- Stores ---
        stores = []
        for _ in range(20):
            store = Store.objects.create(
                name=fake.company(),
                location=fake.city()
            )
            stores.append(store)
        self.stdout.write(self.style.SUCCESS("20+ Stores created."))

        # --- Inventory ---
        for store in stores:
            inventory_products = random.sample(products, 300)
            for prod in inventory_products:
                Inventory.objects.create(
                    store=store,
                    product=prod,
                    quantity=random.randint(1, 100)
                )
        self.stdout.write(self.style.SUCCESS("Inventory created for each store (300+ products)."))
