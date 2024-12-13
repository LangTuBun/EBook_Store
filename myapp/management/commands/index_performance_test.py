from django.core.management.base import BaseCommand
from django.utils.timezone import now
from myapp.models import Orders2
import time

class Command(BaseCommand):
    help = "Compare query execution time with and without an index."

    def handle(self, *args, **options):
        # Generate a large dataset if needed
        if Orders2.objects.count() < 50000:
            self.stdout.write("Generating large dataset...")
            self.generate_demo_data()

        # Run the query without the index
        self.stdout.write("Running query without index...")
        time_without_index = self.measure_query_time()

        # Add the index
        self.stdout.write("Applying index...")
        self.apply_index()

        # Run the query with the index
        self.stdout.write("Running query with index...")
        time_with_index = self.measure_query_time()

        # Display results
        self.stdout.write(f"Query time without index: {time_without_index:.4f} seconds")
        self.stdout.write(f"Query time with index: {time_with_index:.4f} seconds")

    def generate_demo_data(self):
        from django.utils import timezone
        import random

        for i in range(500000):
            Orders2.objects.create(
                order_id=i,
                customer=None,
                employee=None,
                order_date=timezone.now().date(),
                status=random.choice(['Pending', 'Completed', 'Cancelled']),
                from_employee=None
            )

    def measure_query_time(self):
        start_time = time.time()
        # Example query: Filter by status and order_date
        list(Orders2.objects.filter(status="Completed").order_by("order_date"))
        end_time = time.time()
        return end_time - start_time

    def apply_index(self):
        from django.db import connection
        with connection.cursor() as cursor:
            # Check if the index exists
            cursor.execute("""
                SELECT COUNT(1)
                FROM INFORMATION_SCHEMA.STATISTICS
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_NAME = 'orders'
                AND INDEX_NAME = 'idx_orders_status_order_date'
            """)
            index_exists = cursor.fetchone()[0] > 0

            # Drop the index if it exists
            if index_exists:
                cursor.execute("DROP INDEX idx_orders_status_order_date ON orders")

            # Create the index
            cursor.execute("CREATE INDEX idx_orders_status_order_date ON orders (status, order_date)")


# Run the management command