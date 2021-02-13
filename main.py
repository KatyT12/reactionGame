import sqlite3
import time
import datetime
import random

from db_actions import dba #Seperate files to keep code organized
import auth
from auth import validate_int

class Game:
  def __init__(self,username,db):
    self.username = username
    self.db = db
    self.loop()
    
  def loop(self):
    while True:
      print()
      b = self.menu()
      if b:
        break      

  def menu(self):
    num = validate_int("1: Play reaction game\n2:See all results of tests\n3:Get average reaction time\n4:Quit this session\n>",1,4)
    
    print()
    if num == 1:
      self.new_test()
    elif num == 2:
      self.db.print_all_tests_for_user(self.username)
    elif num == 3:
      avg = self.average_reaction_time()
      print("%f seconds" % avg)
    elif num == 4:
      return True
    return False

  def new_test(self):
    reaction = self.get_speed()
    score = reaction[1] * 100000
    db.insert_test(self.username,score,reaction[0])

  def average_reaction_time(self):
    l = db.all_times_of_user(self.username)    
    num = 0
    for n in l:
      num += n
    return num/len(l)    

  def get_speed(self):
    input("Press enter to start and stop.")
    print("Get ready!")
    time.sleep(random.randint(1000,3000)/1000)

    start = datetime.datetime.now()
    input("Go!")
    end = datetime.datetime.now()

    time_id = str(start)
    speed = (end-start).total_seconds()

    test = [time_id,speed]

    return test

if __name__ == "__main__":
  db = dba()
  db.connect_db()
  #db.create_database()

  while True:
    username = auth.authenticate(db)
    if username == False:
      exit(0)
    game = Game(username,db)
  #db.delete_database()
