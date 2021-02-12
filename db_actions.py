import datetime
import sqlite3
import os
import hashlib

class dba:
  DB_NAME = "Reaction.db"
  MAX_PASSWORD_LEN = 30
  conn = 0

  def connect_db(self):
      self.conn = sqlite3.connect(self.DB_NAME)


  def delete_database(self):
      if os.path.exists(self.DB_NAME):
        os.remove(self.DB_NAME)

  def create_database(self):
      string = ('''CREATE TABLE User (
      Username VARCHAR(20) NOT NULL PRIMARY KEY,
      Password CHAR(%d) NOT NULL,
      Age INT NOT NULL
    );''' % self.MAX_PASSWORD_LEN)

      self.conn.execute(string)
      self.conn.execute('''CREATE TABLE Test(
      Username VARCHAR(20) NOT NULL,
      DateTime TIMESTAMP NOT NULL,
      Score FLOAT NOT NULL,
      PRIMARY KEY (Username,DateTime),
      FOREIGN KEY (Username) REFERENCES User(Username)
      );'''
      );
      self.conn.commit()

  def insert_test(self,username,score,date_time):
      string = ('''INSERT INTO Test(Username,DateTime,Score)
      VALUES('%s','%s',%f)''' % (username,date_time,score))
      self.conn.execute(string)
      self.conn.commit()


  def insert_user(self,username,password,age):
      hashed_password = hashlib.sha256(password.encode()).hexdigest()
      string = ('''INSERT INTO User(Username,Password,Age)
      VALUES('%s','%s',%d);''' % (username,hashed_password,age))

      self.conn.execute(string)
      self.conn.commit()

  def check_user_exists(self,username):
    string = ('''SELECT count(username) FROM User 
    WHERE username='%s' ''' % username)
    result = self.conn.execute(string)

    if(result.fetchone()[0] > 0):
      return True
    else:
      return False

  def get_user_password_hash(self,username):
    if not self.check_user_exists(username):
      return -1
    
    string = ('''SELECT Password FROM User
    WHERE username = '%s' ''' % username)
    result = self.conn.execute(string)
    password =  result.fetchone()[0]
    return password

  def get_max_password_length(self):
    return self.MAX_PASSWORD_LEN

  def print_all_users(self):
    u = self.conn.execute("SELECT * FROM User")
    for line in u:
      print(line)
      
  def print_all_tests(self):
    u = self.conn.execute("SELECT * FROM Test")
    for line in u:
      print(line)

  def all_times_of_user(self,username):
    l=[]
    string = ('''SELECT Score/100000 FROM Test WHERE username = '%s' ''' % username)
    u = self.conn.execute(string)
    for i in u:
      l.append(float(i[0]))
    return l

  def print_all_tests_for_user(self,username):
    string = ('''SELECT Username, DateTime, Score FROM Test
    WHERE Username='%s' ''' % username)
    cursor = self.conn.execute(string)
      
    print("Username |      DateTime       |   Score   |")
    print()
    for line in cursor:
      print("%s   %s   %s" % (line[0],line[1],line[2]))