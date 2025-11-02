# 🧩 Python Generators — Task 0: Getting Started

This project introduces **Python Generators** through a practical use-case that connects Python to a MySQL database.  
It demonstrates how to **seed a database**, **stream data row-by-row**, and build the foundation for later tasks that use memory-efficient, lazy iteration.

---

## 🎯 **Objective**

Create a Python script `seed.py` that:

1. Connects to a MySQL server.  
2. Creates the database **`ALX_prodev`** (if it doesn’t exist).  
3. Connects to the new database.  
4. Creates the table **`user_data`** with the required schema:  

   | Field | Type | Constraint |
   | :-- | :-- | :-- |
   | `user_id` | `CHAR(36)` | Primary Key, Indexed |
   | `name` | `VARCHAR(255)` | NOT NULL |
   | `email` | `VARCHAR(255)` | NOT NULL |
   | `age` | `DECIMAL(5,0)` | NOT NULL |

5. Populates the table with sample records from **`user_data.csv`**.

---

## 🧠 **Learning Concepts**

- Working with **MySQL** using `mysql-connector-python`.  
- Creating and seeding a relational database programmatically.  
- Handling CSV files with Python’s built-in `csv` module.  
- Writing reusable database utility functions:
  - `connect_db()`
  - `create_database(connection)`
  - `connect_to_prodev()`
  - `create_table(connection)`
  - `insert_data(connection, csv_path)`

---

## ⚙️ **Requirements**

- Python 3.8 or newer  
- MySQL Server 5.7 or 8.x  
- Install the MySQL connector:

  ```bash
  pip install mysql-connector-python
