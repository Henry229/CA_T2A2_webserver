# API Web server for HR management
## R1 - The purpose of the Application
The HR management system is used as an important tool for strategic personnel management. It is an integrated HR management system that helps effective decision-making through integrated data management. Support performance management of each employee and increase employee satisfaction.<br>Therefore, the HR department is intended to manage all employees in the company effectively. You can see at a glance the wages, job positions, dates of employment, and departments of workers. When a request to create, modify, or delete an employee from the frontend page of HR management system, each API in this application can manipulate the employee's data in the database.<br>
This application is accessible only to staffs working at the HR department. This is because there is sensitive private information of workers.

----
<br>

## R2 -Why is it a problem that needs solving?
A company that manages employees will have a demand to manage employees efficiently. There is a need for a management system that allows employees to focus on their work, such as employee's department movement, current salary, and current department.<br>
Without such a system, it becomes very difficult to respond when creating next year's budget, creating new departments, or eliminating existing departments.<br> Therefore, this application is needed for CEO or staff in the HR department to make decisions quickly and manage employees efficiently.

----
<br>

## R3 - Why have you chosen this database system. What are the drawbacks compared to others?
<br>
The most important characteristic of using a database to create a system is that it manages structured data. Data can be organised in columns such as 'ID' and 'password', sorted by some criteria, and filtered. Therefore, using the database to create this application is because adding/updating/deleting/retrieving data is more structured and faster. Among them, the reason RDB such as PostgreSQL was selected is that it is very suitable for the main database for providing service. In addition, <u>all the schema and db models of this application are fixed and will be used within the HR dapartment, so it does not need extremely high speed.</u> 
<br><br>

### comparison to No SQL database 

Because NoSQL is 'schemaless', data can be stored more flexibly, but RDBs used by this application rarely have schema change. On average, it is true that NoSQL is faster than RDB, and when using the same cost, NoSQL database is cost-effective in terms of performance. But this depends on which RDB you use.<br>
NoSQL is recommended when the exact data structure is unknown and data can be changed or expanded. However, if data duplication can occur, all collections must be modified when duplicate data is changed, so it is good for systems that do not have many updates. On the other hand, because RDB guarantees data integrity and is easy to change, it is suitable for this application where related data is frequently changed.

### Pros and Cons of RDB

#### Benefits
As I mentioned above, data should be saved according to the established schema, ensuring a clear dta structure. There is no duplication of data, so data consistency can be guaranteed.

#### Drawbacks
As the system grows, complex queries with many JOIN statement will make the system slow down. If you want to add columns in tables having a lot of data, you must alter table and create a new table. Moreover, improving hardware performance can be costly.

Reference: https://peps.python.org/pep-0008/ <br>
Reference: https://docs.rackspace.com/support/how-to/choosing-between-rdbms-and-nosql/
____
<br>

## R4 - Identify and discuss the key functionalities and benefits of an ORM
<br>

### What is ORM?
ORM(Object-Relational Mapping) is simply setting connections between objects in object_oriented programs and relational database. To use RDB, you must use SQL. However, ORM automatically converts the written Python code into a SQL query of the relational DB, allowing developers to manipulate the DB only by writing Python code without having to write a separate SQL query. For example, below is an example of a SQLAlchemy model definition. We create a class named Contact with SQLAlchemy
```py 
  class Contact(db.Model):
      __tablename__ = 'contacts'
      id = db.Column(db.Integer, primary_key=True)
      first_name = db.Column(db.String(100))
      last_name = db.Column(db.String(100))
      phone_number = db.Column(db.String(32)) 
```
If we do the migration, we can get a Contact table in Database even though we don't write any create table statement. 
```py
  CREATE TABLE CONTACTS(
      ID INT PRIMARY KEY        NOT NULL,
      FIRST_NAME     CHAR(100)  NOT NULL,
      LAST_NAME      CHAR(100)  NOT NULL,
      PHONE_NUMBER   CHAR(32)   NOT NULL,
);
```
Reference: https://www.fullstackpython.com/sqlalchemy.html<br><br>

SQLAlchemy handle the table creation by using ORM. IT can be seen a table create statement was created so that a table could be created just like the class.<br>
In addition, all records can be retrieved by using SQLAlchemy in Python code such as `contacts = Contact.query.all()` instead of a plain SQL, `SELECT * FROM contacts`. 

#### Benefits of ORM
No need to create declaration, assignment in programs, so we can reduce development time. Once you write your data model, ORM creates Table automatically so we can improve the productivity. Also Model use OOP(Object-Oriented Programming), we can speed up development by extending and inheriting from Models. SQL injection is not easy as queries are sanitised.<br>

Reference: https://www.freecodecamp.org/news/what-is-an-orm-the-meaning-of-object-relational-mapping-database-tools/<br>
Reference: https://www.learnnowonline.com/blogs/2012/08/28/4-benefits-of-object-relational-mapping-orm<br>
Reference: https://midnite.uk/blog/the-pros-and-cons-of-object-relational-mapping-orm

----
<br>

## R5 - Document all endpoints for your API

<br>

- Login
  - HTTP request verb : POST
  - Required data where applicable : The email and password are needed in JSON
  - Expected response data : The email, encoded password and token using JWT
  - Authentication methods where applicable: n/a

<br>

- Get all HR staffs
  - HTTP request verb : GET
  - Required data where applicable : N/A
  - Expected response data : 'id', 'is_admin', 'employees', 'employee_id', 'email'
  - Authentication methods where applicable: N/A

<br>

- Get a HR staff
  - HTTP request verb : GET
  - Required data where applicable : id parameter
  - Expected response data : 'id', 'is_admin', 'employees', 'employee_id', 'email'
  - Authentication methods where applicable: N/A

<br>

- Add a new HR staff
  - HTTP request verb : POST
  - Required data where applicable : employee_id, is_admin
  - Expected response data : 'id', 'is_admin', 'employees', 'employee_id', 'email'
  - Authentication methods where applicable: Token by JWT

<br>

- Delete a HR staff
  - HTTP request verb : DELETE
  - Required data where applicable : id parameter
  - Expected response data : Delete confirmation message
  - Authentication methods where applicable: Token by JWT

<br>

- Update a HR staff
  - HTTP request verb : PUT
  - Required data where applicable : One of fields in hrstaffs table and id parameter- 
  - Expected response data : 'id', 'is_admin', 'employees', 'employee_id', 'email'
  - Authentication methods where applicable: Token by JWT

<br>

- Get all employees
  - HTTP request verb : GET
  - Required data where applicable : N/A
  - Expected response data : 'id', 'name', 'email', 'password', 'salary','hire_date', 'job_id', 'department_id', 'job', 'department'
  - Authentication methods where applicable: N/A
  
<br>

- Get a employee
  - HTTP request verb : GET
  - Required data where applicable : id parameter
  - Expected response data : 'id', 'name', 'email', 'password', 'salary','hire_date', 'job_id', 'department_id', 'job', 'department'
  - Authentication methods where applicable: N/A

<br>

- Add a new employee
  - HTTP request verb : POST
  - Required data where applicable : All fields of employees table
  - Expected response data : 'id', 'name', 'email', 'password', 'salary','hire_date', 'job_id', 'department_id', 'job', 'department'
  - Authentication methods where applicable: Token by JWT

<br>

- Delete a employee
  - HTTP request verb : DELETE
  - Required data where applicable : id parameter
  - Expected response data : Delete confirmation message
  - Authentication methods where applicable: Token by JWT

<br>

- Update a employee
  - HTTP request verb : PUT
  - Required data where applicable : fields of employees that need to update and id parameter
  - Expected response data : 'id', 'name', 'email', 'password', 'salary','hire_date', 'job_id', 'department_id', 'job', 'department'
  - Authentication methods where applicable: Token by JWT

<br>


- Get all department
  - HTTP request verb : GET
  - Required data where applicable : N/A
  - Expected response data : 'id', 'department_name'
  - Authentication methods where applicable: N/A

<br>

- Get a department
  - HTTP request verb : GET
  - Required data where applicable : id parameter
  - Expected response data : 'id', 'department_name'
  - Authentication methods where applicable: N/A

<br>


- Add a department
  - HTTP request verb : POST
  - Required data where applicable : fields in departments table
  - Expected response data : 'id', 'department_name'
  - Authentication methods where applicable: Token by JWT

<br>

- Delete a department
  - HTTP request verb : DELETE
  - Required data where applicable : id parameter
  - Expected response data : Delete confirmation message
  - Authentication methods where applicable: Token by JWT
  
<br>

- Update a department
  - HTTP request verb : PUT
  - Required data where applicable : fields of department table that need to update and id parameter
  - Expected response data : 'id', 'name', 'email', 'password', 'salary','hire_date', 'job_id', 'department_id', 'job', 'department'
  - Authentication methods where applicable: Token by JWT


<br>

- Get all jobs
  - HTTP request verb : GET
  - Required data where applicable : N/A
  - Expected response data : 'id', 'job_position'
  - Authentication methods where applicable: N/A

<br>

- Get a  job
  - HTTP request verb : GET
  - Required data where applicable : id parameter
  - Expected response data : 'id', 'job_position'
  - Authentication methods where applicable: N/A

<br>

- Add a new job
  - HTTP request verb : GET
  - Required data where applicable : id parameter
  - Expected response data : 'id', 'job_position'
  - Authentication methods where applicable: N/A

<br>

- Update a job
  - HTTP request verb : PUT
  - Required data where applicable : fields in jobs table need to update
  - Expected response data : 'id', 'job_position',
  - Authentication methods where applicable: Token by JWT

<br>

- Delete a job
  - HTTP request verb : DELETE
  - Required data where applicable : id parameter
  - Expected response data : Delete confirmation message
  - Authentication methods where applicable: Token by JWT

<br>

---


