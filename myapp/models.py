# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models




class Author(models.Model):
    author_id = models.IntegerField(db_column='Author_id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    nationality = models.CharField(db_column='Nationality', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'author'


class Book(models.Model):
    book_id = models.IntegerField(db_column='Book_id', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=255)  # Field name made lowercase.
    price = models.DecimalField(db_column='Price', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    language = models.CharField(db_column='Language', max_length=50, blank=True, null=True)  # Field name made lowercase.
    availability_status = models.CharField(db_column='Availability_Status', max_length=20, blank=True, null=True)  # Field name made lowercase.
    publisher = models.ForeignKey('Publisher', models.DO_NOTHING, db_column='Publisher_id', blank=True, null=True)  # Field name made lowercase.
    author = models.ForeignKey(Author, models.DO_NOTHING, db_column='Author_ID', blank=True, null=True)  # Field name made lowercase.
    category_id = models.CharField(db_column='Category_id', max_length=20, blank=True, null=True)  # Field name made lowercase.
    amount = models.IntegerField(db_column='Amount', blank=True, null=True)  # Field name made lowercase.
    publishdate = models.DateTimeField(db_column='PublishDate', blank=True, null=True)  # Field name made lowercase.
    img_url = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book'


class BookCoupon(models.Model):
    book = models.ForeignKey(Book, models.DO_NOTHING)
    coupon_code = models.CharField(primary_key=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'book_coupon'


class Category(models.Model):
    category_id = models.IntegerField(db_column='Category_id', primary_key=True)  # Field name made lowercase.
    category_name = models.CharField(db_column='Category_Name', max_length=50)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'category'


class Coupon(models.Model):
    coupon_code = models.CharField(primary_key=True, max_length=20)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    valid_until = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coupon'


class Customer(models.Model):
    customer_id = models.IntegerField(db_column='Customer_id', primary_key=True)  # Field name made lowercase.
    account = models.ForeignKey('User', models.DO_NOTHING, db_column='Account_id', blank=True, null=True)  # Field name made lowercase.
    discount_id = models.IntegerField(db_column='Discount_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'customer'


class CustomerCoupon(models.Model):
    customer = models.OneToOneField(Customer, models.DO_NOTHING, primary_key=True)  # The composite primary key (customer_id, coupon_code) found, that is not supported. The first column is selected.
    coupon_code = models.ForeignKey(BookCoupon, models.DO_NOTHING, db_column='coupon_code')
    redeem_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_coupon'
        unique_together = (('customer', 'coupon_code'),)




class Employee(models.Model):
    employee_id = models.IntegerField(db_column='Employee_id', primary_key=True)  # Field name made lowercase.
    account = models.ForeignKey('User', models.DO_NOTHING, db_column='Account_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'employee'


class OrderDetail(models.Model):
    order_detail_id = models.IntegerField(db_column='Order_detail_id', primary_key=True)  # Field name made lowercase.
    order = models.ForeignKey('Orders', models.DO_NOTHING, db_column='Order_id', blank=True, null=True)  # Field name made lowercase.
    book = models.ForeignKey(Book, models.DO_NOTHING, db_column='Book_id', blank=True, null=True)  # Field name made lowercase.
    quantity = models.IntegerField(db_column='Quantity', blank=True, null=True)  # Field name made lowercase.
    price_each = models.DecimalField(db_column='Price_each', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'order_detail'


class Orders(models.Model):
    order_id = models.IntegerField(db_column='Order_id', primary_key=True)  # Field name made lowercase.
    customer = models.ForeignKey(Customer, models.DO_NOTHING, db_column='Customer_id', blank=True, null=True)  # Field name made lowercase.
    employee = models.ForeignKey(Employee, models.DO_NOTHING, db_column='Employee_id', blank=True, null=True)  # Field name made lowercase.
    order_date = models.DateField(db_column='Order_date', blank=True, null=True)  # Field name made lowercase.
    shipped_date = models.DateField(db_column='Shipped_Date', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=20, blank=True, null=True)  # Field name made lowercase.
    from_employee = models.IntegerField(db_column='From_employee', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'orders'


class Payments(models.Model):
    payment_id = models.IntegerField(db_column='Payment_id', primary_key=True)  # Field name made lowercase.
    order = models.ForeignKey(Orders, models.DO_NOTHING, db_column='Order_id', blank=True, null=True)  # Field name made lowercase.
    payment_method = models.CharField(db_column='Payment_method', max_length=50, blank=True, null=True)  # Field name made lowercase.
    payment_date = models.DateField(db_column='Payment_date', blank=True, null=True)  # Field name made lowercase.
    amount = models.DecimalField(db_column='Amount', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    payment_status = models.CharField(db_column='Payment_status', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'payments'


class Publisher(models.Model):
    publisher_id = models.IntegerField(db_column='Publisher_id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    address = models.TextField(db_column='Address', blank=True, null=True)  # Field name made lowercase.
    contact_info = models.TextField(db_column='Contact_info', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'publisher'


class Reviews(models.Model):
    review_id = models.IntegerField(db_column='Review_id', primary_key=True)  # Field name made lowercase.
    book = models.ForeignKey(Book, models.DO_NOTHING, db_column='Book_id', blank=True, null=True)  # Field name made lowercase.
    rating = models.FloatField(db_column='Rating', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'reviews'


class User(models.Model):
    account_id = models.IntegerField(db_column='Account_id', primary_key=True)  # Field name made lowercase.
    user_name = models.CharField(db_column='User_name', max_length=50)  # Field name made lowercase.
    first_name = models.CharField(db_column='First_name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    last_name = models.CharField(db_column='Last_name', max_length=50, blank=True, null=True)  # Field name made lowercase.
    address = models.TextField(db_column='Address', blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=255)  # Field name made lowercase.
    registered_date = models.DateField(db_column='Registered_date', blank=True, null=True)  # Field name made lowercase.
    from_employee = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
        
    @property
    def is_authenticated(self):
        # Since you're using a custom authentication backend,
        # you can define your own logic for authentication
        return self.account_id is not None
    @classmethod
    def with_roles(cls, account_id, is_customer, is_employee):
        user = cls.objects.get(account_id=account_id)
        return user


class UserProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    image = models.CharField(max_length=100)
    user = models.OneToOneField(User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'user_profile'
