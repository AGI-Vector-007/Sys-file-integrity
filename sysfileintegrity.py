

import hashlib
import os
import time
"""# **Generating the file hash**"""

def generate_file_hash(file_path):
  hash = hashlib.sha256()
  with open(file_path,"rb") as file:
    buffer = file.read()
    hash.update(buffer)
  return hash.hexdigest()

"""# **Creating a baseline for all directory**"""

def baseline(dir)->dict:
  bsline = {}
  for root, dirs, files in os.walk(dir):
    for file in files:
      # joining the path
      file_path = os.path.join(root, file)
      # generating the hash
      file_hash = generate_file_hash(file_path)
      bsline[file_path] = file_hash
  return bsline

"""# ***Saving the baseline files in a txt file.***"""

dir_monitor = input("Specify the File path:") or os.getcwd()
baseline_hash = baseline(dir_monitor)
with open("baseline.txt","w") as file:
  for f_path,f_hash in baseline_hash.items():
    file.write(f"{f_path},{f_hash}\n")

"""# **Writing a Monitor to check the integrity of the files.**"""



def monitor(dir,baseline_hash_file="baseline.txt"):
  with open(baseline_hash_file,"r") as file:
    bline = dict(l.strip().split(",") for l in file)
  while True:
    for root,dirs,files in os.walk(dir):
      for file in files:
        file_path = os.path.join(root,file)
        current_hash = generate_file_hash(file_path)
        if file_path in bline:
          if current_hash!=bline[file_path]:
            print("[Warning!!]File Integrity has been breached\nFile has been modified")
            print(f"File: {file_path}")
            print(f"Original Hash: {bline[file_path]}")
            print(f"Current Hash: {current_hash}")
        else:
          print("[@Alert]File Integrity has been breached\nNew File has been added")
    # 60 second break for every file check.
    time.sleep(10)

monitor(dir_monitor)
