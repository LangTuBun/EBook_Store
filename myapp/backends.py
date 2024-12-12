from django.contrib.auth.backends import BaseBackend
from myapp.models import User, Customer, Employee
from django.contrib.auth.hashers import check_password, make_password
from django.db import IntegrityError, transaction, Error
from django.db import connection
import random
import logging
logger = logging.getLogger(__name__)

class CustomRoleBackend(BaseBackend):

    def generate_unique_customer_id(self):
        while True:
            # Generate a random 5-digit customer ID
            customer_id = random.randint(10000, 99999)
            
            # Check if the generated customer_id already exists in the Customer table
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1 FROM CUSTOMER WHERE customer_id = %s", [customer_id])
                if not cursor.fetchone():
                    return customer_id  # Return if the ID is unique
    
    def add_user(self, user_name, first_name, last_name, address, password, registered_date, is_employee=False):
        try:
            # Hash the password
            hashed_password = make_password(password)
            # Generate a unique customer_id for the new user
            cursor = connection.cursor()
            cursor.execute("SELECT MAX(account_id) FROM USER")
            account_id = cursor.fetchone()
            if account_id[0] is None:
                account_id = 1
            else:
                account_id = account_id[0] + 1
            customer_id = self.generate_unique_customer_id()
            print(account_id,customer_id)
            # Insert the user into the USER table
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO USER (account_id, user_name, first_name, last_name, address, password, registered_date)
                        VALUES (%s,%s, %s, %s, %s, %s, %s)
                        """, [account_id,user_name, first_name, last_name, address, hashed_password, registered_date]
                    )
            except Error as e:
                print(f"Error: {e}")
                # Get the auto-generated account_id
            # Insert into the Customer or Employee table based on the `is_employee` flag
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO CUSTOMER (customer_id, account_id)
                    VALUES (%s, %s)
                    """, [customer_id, account_id]
                )

            # Return True if user and associated role are successfully created
            return True

        except IntegrityError as e:
            # Handle database integrity errors (e.g., duplicate user_name)
            print(f"Error: {e}")
            return None
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            print('Custom backend is being called')
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT u.account_id, u.password, c.customer_id, e.employee_id
                    FROM USER u
                    LEFT JOIN CUSTOMER c ON u.account_id = c.account_id
                    LEFT JOIN EMPLOYEE e ON u.account_id = e.account_id
                    WHERE u.user_name = %s
                """, [username])
                result = cursor.fetchone()

            if result:
                account_id, hashed_password, customer_id, employee_id = result
                if employee_id:
                    if password == password:  # Check regular password
                        is_employee = employee_id is not None
                        is_customer = customer_id is not None
                        return User.with_roles(account_id, is_customer, is_employee)
                else:
                    if check_password(password, hashed_password):  # Check hashed password
                        is_customer = customer_id is not None
                        is_employee = employee_id is not None
                        return User.with_roles(account_id, is_customer, is_employee)

        except Exception as e:
            print(f"Authentication error: {e}")
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None