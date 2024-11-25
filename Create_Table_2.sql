-- Publishers table
CREATE TABLE Publisher (
    Publisher_id INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Address TEXT,
    Contact_info TEXT
);

-- Authors table
CREATE TABLE Author (
    Author_id INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Nationality VARCHAR(50)
);
-- Categories table
CREATE TABLE Category (
    Category_id INT PRIMARY KEY,
    Category_Name VARCHAR(50) NOT NULL,
    Description TEXT
);

-- Books table
CREATE TABLE Book (
    Book_id INT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Price DECIMAL(10,2),
    Language VARCHAR(50),
    Availability_Status VARCHAR(20),
    Publisher_id INT,
    Author_ID INT,
    Category_id VARCHAR(20),
    Amount INT,
    PublishDate INT,
    FOREIGN KEY (Publisher_id) REFERENCES Publisher(Publisher_id),
    FOREIGN KEY (Author_ID) REFERENCES Author(Author_ID)
);


-- Users table
CREATE TABLE User (
    Account_id INT PRIMARY KEY,
    User_name VARCHAR(50) NOT NULL,
    First_name VARCHAR(50),
    Last_name VARCHAR(50),
    Address TEXT,
    Password VARCHAR(255) NOT NULL,
    Registered_date DATE,
    from_employee BOOLEAN DEFAULT 0
);

-- Employees table (extends User)
CREATE TABLE Employee (
    Employee_id INT PRIMARY KEY,
    Account_id INT,
    FOREIGN KEY (Account_id) REFERENCES User(Account_id)
);

-- Customers table
CREATE TABLE Customer (
    Customer_id INT PRIMARY KEY,
    Account_id INT,
    Discount_id INT,
    FOREIGN KEY (Account_id) REFERENCES User(Account_id)
);

-- Orders table
CREATE TABLE Orders (
    Order_id INT PRIMARY KEY,
    Customer_id INT NULL,
    Employee_id INT NULL,
    Order_date DATE,
    Shipped_Date DATE,
    Status VARCHAR(20),
    From_employee BOOLEAN DEFAULT 0,
    FOREIGN KEY (Customer_id) REFERENCES Customer(Customer_id) ON DELETE CASCADE,
    FOREIGN KEY (Employee_id) REFERENCES Employee(Employee_id) ON DELETE CASCADE
);

-- Order details table
CREATE TABLE Order_Detail (
    Order_detail_id INT PRIMARY KEY,
    Order_id INT,
    Book_id INT,
    Quantity INT,
    Price_each DECIMAL(10,2),
    FOREIGN KEY (Order_id) REFERENCES Orders(Order_id) ON DELETE CASCADE,
    FOREIGN KEY (Book_id) REFERENCES Book(Book_id) ON DELETE CASCADE
);

-- Book discounts table
CREATE TABLE book_coupon (
    book_id INT NOT NULL,
    coupon_code VARCHAR(20) NOT NULL UNIQUE,
    PRIMARY KEY (book_id, coupon_code),
    FOREIGN KEY (book_id) REFERENCES book(book_id)
);

CREATE TABLE coupon (
    coupon_code VARCHAR(20) NOT NULL PRIMARY KEY,
    discount_percentage DECIMAL(5, 2),
    valid_until DATE
);


-- Customer discounts table
CREATE TABLE customer_coupon (
    customer_id INT NOT NULL,
    coupon_code VARCHAR(20) NOT NULL,
    redeem_date DATE,
    PRIMARY KEY (customer_id, coupon_code),
    FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    FOREIGN KEY (coupon_code) REFERENCES book_coupon(coupon_code)
    
);
-- Reviews table
CREATE TABLE Reviews (
    Review_id INT PRIMARY KEY,
    Book_id INT,
    Rating INT,
    FOREIGN KEY (Book_id) REFERENCES Book(Book_id)
);

-- Payments table
CREATE TABLE Payments (
    Payment_id INT PRIMARY KEY,
    Order_id INT,
    Payment_method VARCHAR(50),
    Payment_date DATE,
    Amount DECIMAL(10,2),
    Payment_status VARCHAR(20),
    FOREIGN KEY (Order_id) REFERENCES Orders(Order_id) ON DELETE CASCADE
);


