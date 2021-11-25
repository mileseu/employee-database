import sqlite3
import pandas as pd
from collections import Counter

#DBOperation class to manage all data into the database. 
class DBOperations:
  sql_create_table_firsttime = '''CREATE TABLE IF NOT EXISTS employee (
    EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title VARCHAR(20),
    Forename VARCHAR(20),
    Surname VARCHAR(20),
    Email VARCHAR(20),
    Salary integer
  )'''
  sql_create_table = '''CREATE TABLE employee (
    EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title VARCHAR(20),
    Forename VARCHAR(20),
    Surname VARCHAR(20),
    Email VARCHAR(20),
    Salary integer
  )'''
  sql_insert = '''
    INSERT INTO employee(title, forename, surname, email, salary)
    VALUES (?,?,?,?,?)
    '''
  sql_select_all = "select * from employee"
  sql_search = "select * from employee where employeeID=(?)"
  sql_delete_data = "DELETE FROM employee WHERE employeeID=(?)"
  sql_drop_table = "DROP TABLE employee"
 
  def __init__(self):
    try:
      self.conn = sqlite3.connect("employee.db")
      self.cur = self.conn.cursor()
      self.cur.execute(self.sql_create_table_firsttime)
      self.conn.commit()
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def get_connection(self):
    self.conn = sqlite3.connect("employee.db")
    self.cur = self.conn.cursor()

  def create_table(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_create_table)
      self.conn.commit()
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def insert_data(self):
    try:
      self.get_connection()
      emp = Employee()
      emp.set_employee_title(input("Enter Employee Title: "))
      emp.set_forename(input("Enter Employee Forename: "))
      emp.set_surname(input("Enter Employee Surname: "))
      emp.set_email(input("Enter Employee Email: "))
      emp.set_salary(input("Enter Employee Salary: "))
      self.cur.execute(self.sql_insert, (emp.empTitle, emp.forename, emp.surname, emp.email, emp.salary))
      self.conn.commit()
      print("Inserted data successfully")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def select_all(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_select_all)
      #pandas used for easy formatting and alignment
      allData = pd.read_sql_query(self.sql_select_all, self.conn)
      self.conn.commit()
      print(allData)
    except Exception as e:
      print(e)
    finally:
      self.conn.close()
    
  def search_data(self):
    try:
      self.get_connection()
      employeeID = int(input("Enter Employee ID: "))
      #employee row print helper function
      self.printRow(employeeID)
      self.conn.commit()
    except Exception:
      print("Invalid EmployeeID")
    finally:
      self.conn.close()

  def search_by_column(self):
    try:
      self.get_connection()
      #column choices given, returns column as string
      column=self.column_choice()
      if column != "return":
        search = input("Enter search term: ")
        #query outside of DBops due to local var
        query = 'SELECT * from employee WHERE '+column+' = ?'
        self.cur.execute(query,(search,))
        result = self.cur.fetchall()
        self.conn.commit()
        #Counter package used just to print result count
        c = Counter(search for elem in result)
        #sum could return incorrectly if row has duplicate values, not vital but could be improved
        count = sum(c.values())
        if result:
          print(count, "record(s) found:\n")
          for row in result:
            self.printRow(row[0])
        else:
          print("No record")
      else:
        print("Returning to menu")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def update_data(self):
    try:
      self.get_connection()
      employeeID = int(input("Enter Employee ID: "))
      if self.printRow(employeeID):
        print("Record selected to update.\n")
        column=self.column_choice()
        if column != "return":
          value=input("Enter new value: ")
          #query outside of DBops due to local var
          query='UPDATE employee SET '+column+' = ? WHERE employeeID = ?'
          self.cur.execute(query,(value, str(employeeID)))
          self.conn.commit()
          print("Record updated successfully")
        else:
          print("Returning to menu")
    except Exception:
      print("Invalid EmployeeID or column")
    finally:
      self.conn.close()

  def delete_data(self):
    try:
      self.get_connection()
      employeeID = int(input("Enter Employee ID: "))
      if self.printRow(employeeID):
        print("Record selected, delete? (y/n)")
        choice = input()
        if choice == "y":
          self.cur.execute(self.sql_delete_data,(employeeID,))
          self.conn.commit()
          print("Deleted data successfully")
        else:
          print("Delete cancelled")

    except Exception:
      print("Invalid EmployeeID")
    finally: 
      self.conn.close()

  def drop_table(self):
    try:
      self.get_connection()
      print("WARNING! This will delete all employee records.\nEnter DELETE to continue or QUIT to cancel")
      choice = input()
      if choice == "DELETE":
        self.cur.execute(self.sql_drop_table)
        self.conn.commit()
        print("Records successfully deleted")
      else:
        print("Records not deleted")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

#helper function, lets user pick column
  def column_choice(self):
    print ("\n Pick attribute:")
    print ("**********")
    print (" 1. EmployeeID")
    print (" 2. Title")
    print (" 3. Forename")
    print (" 4. Surname")
    print (" 5. Email")
    print (" 6. Salary")
    print (" 7. Exit\n")
    
    try:
      __header_menu = int(input("Enter your choice: "))
      if __header_menu == 1:
        return "employeeID"
      elif __header_menu == 2:
        return "title"
      elif __header_menu == 3:
        return "forename"
      elif __header_menu == 4:
        return "surname"
      elif __header_menu == 5:
        return "email"
      elif __header_menu == 6:
        return "salary"
      elif __header_menu == 7:
        return "return"
      else:
        print ("Invalid Choice")
        return "return"
    except Exception:
      print("Invalid Choice")
      return "return"

#helper function, takes employeeID and prints info
  def printRow(self, employeeID):
    try:
      self.cur.execute(self.sql_search,(employeeID,))
      result = self.cur.fetchone()
      if type(result) == type(tuple()):
        for index, detail in enumerate(result):
          if index == 0:
            print("Employee ID: " + str(detail))
          elif index == 1:
            print("Employee Title: " + detail)
          elif index == 2:
            print("Employee Name: " + detail)
          elif index == 3:
            print("Employee Surname: " + detail)
          elif index == 4:
            print("Employee Email: " + detail)
          else:
              print("Salary: "+ str(detail)+"\n")
              return True
      else:
        print ("No Record")
        return False
    except Exception as e:
      print(e)

class Employee:
  def __init__(self):
    self.employeeID = 0
    self.empTitle = ''
    self.forename = ''
    self.surname = ''
    self.email = ''
    self.salary = 0.0

  def set_employee_id(self, employeeID):
    self.employeeID = employeeID

  def set_employee_title(self, empTitle):
    self.empTitle = empTitle

  def set_forename(self,forename):
   self.forename = forename
  
  def set_surname(self,surname):
    self.surname = surname

  def set_email(self,email):
    self.email = email
  
  def set_salary(self,salary):
    self.salary = salary
  
  def get_employee_id(self):
    return self.employeeId

  def get_employee_title(self):
    return self.empTitle
  
  def get_forename(self):
    return self.forename
  
  def get_surname(self):
    return self.surname
  
  def get_email(self):
    return self.email
  
  def get_salary(self):
    return self.salary

  def __str__(self):
    return str(self.employeeID)+"\n"+self.empTitle+"\n"+ self.forename+"\n"+self.surname+"\n"+self.email+"\n"+str(self.salary)
  
while True:
  print ("\n Menu:")
  print ("**********")
  print (" 1. Create table EmployeeABC")
  print (" 2. Insert data into EmployeeABC")
  print (" 3. Select all data into EmployeeABC")
  print (" 4. Search an employee")
  print (" 5. Search an employee by attribute")
  print (" 6. Update data some records")
  print (" 7. Delete data some records")
  print (" 8. Delete all records")
  print (" 9. Exit\n")

  try:
    __choose_menu = int(input("Enter your choice: "))
    db_ops = DBOperations()
    if __choose_menu == 1:
      db_ops.create_table()
    elif __choose_menu == 2:
      db_ops.insert_data()
    elif __choose_menu == 3:
      db_ops.select_all()
    elif __choose_menu == 4:
      db_ops.search_data()
    elif __choose_menu == 5:
      db_ops.search_by_column()
    elif __choose_menu == 6:
      db_ops.update_data()
    elif __choose_menu == 7:
      db_ops.delete_data()
    elif __choose_menu == 8:
      db_ops.drop_table()
    elif __choose_menu == 9:
      print("Exiting program")
      exit(0)
    else:
      print ("Invalid choice")
  except Exception:
      print("Invalid choice")