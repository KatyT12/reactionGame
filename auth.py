import hashlib

def login(db):
  exit = False
  valid = False
  
  while not valid and not exit:
    username_input = input("Input your username: ")
    password_input = input("Input your password: ")
    exists = db.check_user_exists(username_input)  
    if not exists:
      print("ERROR: That username does not exist")
      continue
    hashed_password = db.get_user_password_hash(username_input)
    if(str(hashlib.sha256(password_input.encode()).hexdigest()) == hashed_password):
      valid = True
      return username_input
    else:
      print("ERROR: That password is incorrect")
    quit = input("type Q to quit or just press enter to try again")
    if quit == 'Q':
      exit = True
  
  return ""
  
def sign_up(db):
  username = input("Input your username: ")
  if db.check_user_exists(username):
    print("ERROR: That username already exists")
    return ""
  password = input("Input your password for this account. It needs atleast 8 characters and a number in it\n> ")
  #Make sure password is valid according to guidelines
  if len(password) < 8 or len(password) > db.MAX_PASSWORD_LEN:
    print("ERROR: Length of password is invalid")
    return ""
  contains_num = any(chr.isdigit() for chr in password)
  if contains_num:
    age = validate_int("Input your age\n>",0,150)
    db.insert_user(username,password,age)
    return username
  else:
    print("ERROR: password needs to contain a number")
    return ""



def authenticate(db):
  while True:
    option = validate_int("1: Login \n2: Sign up\n3: Quit\n>",1,3)
    username = ""
    if option == 1:
      username = login(db)
    if option == 2:
      username = sign_up(db)
    if option == 3:
      return False
    if username != "":  
        return username
    

def validate_int(message,min=1,max=2):
  while True:
    user = input(message)
    try:
      user = int(user)
      if user >= min and user <= max:
        return user
      else:
        print("ERROR: Invalid range")
    except Exception:
      print("ERROR: Input is invalid") 