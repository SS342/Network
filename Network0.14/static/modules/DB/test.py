import os
path = os.getcwd() + "/static/img/avatars/"
num_files = len([f for f in os.listdir(path)if os.path.isfile(os.path.join(path, f))])
print(num_files)