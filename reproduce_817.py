from rope.base.project import Project
from rope.refactor.inline import InlineVariable

project = Project('.', ropefolder=None)
file = project.root.create_file('file.py')
file.write('''\
s = None
print(s)

def _[T: (A, B)](x):
    pass
''')
try:
    changes = InlineVariable(project, file, 0).get_changes('s')
    project.do(changes)
    print(file.read())
finally:
    file.remove()
    project.close()