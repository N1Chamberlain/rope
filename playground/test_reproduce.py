# made by Connor M. - I made this to familiarize myself with Rope.

from rope.base.project import Project
from rope.refactor.rename import Rename

# 1. create a test project folder
project_path = "playground_project"
import os
os.makedirs(project_path, exist_ok=True)

#2. create a Rope project inside that folder
project = Project(project_path)

# 3. create a simple Python file
file_path = os.path.join(project_path, "a.py")
with open(file_path, "w") as f:
    f.write("""
class A:
    def hello(self):
        print("hi")
        
a = A()
a.hello()
    """)

# 4. load the file in Rope
py_file = project.get_file("a.py")

# 4.5 find offset of 'hello'
source = py_file.read()
offset = source.find("hello")

# 5. prepare a rename refactor for 'hello'
rename = Rename(project, py_file, offset)
changes = rename.get_changes("greet")
project.do(changes)

# 6. confirm result
with open(file_path, "r") as f:
    print(f.read())

#7. cleanup
project.close()