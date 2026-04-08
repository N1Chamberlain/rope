import rope.base.project as project
import rope.refactor.rename as rename
import os

project_root = os.path.dirname(os.path.abspath(__file__))  # automatically uses the repo root

blob_src = open(os.path.join(project_root, "main", "blob.py")).read()

proj = project.Project(project_root)
resource = proj.get_resource("main/blob.py")

offset = blob_src.index("def count") + len("def ")
print(f"Renaming 'count' at offset {offset}")

renamer = rename.Rename(proj, resource, offset)
changes = renamer.get_changes("start_index")

print("\nChanges Rope wants to make:")
print(changes.get_description())

proj.close()