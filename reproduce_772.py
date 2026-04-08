import rope.base.project as project
import rope.refactor.rename as rename
import rope.refactor.occurrences as occurrences
import rope.base.evaluate as evaluate
import rope.base.pynames as pynames
from rope.base.builtins import BuiltinClass
import os

# RENAME REPRODUCTION CODE

project_root = os.path.dirname(os.path.abspath(__file__))  # automatically uses the repo root

blob_src = open(os.path.join(project_root, "main", "blob.py")).read()

proj = project.Project(project_root)
resource = proj.get_resource("main/blob.py")

offset = blob_src.index("def count") + len("def ")
print(f"Renaming 'count' at offset {offset}")

renamer = rename.Rename(proj, resource, offset)
changes = renamer.get_changes("start_index", in_hierarchy=True)

print("\nChanges Rope wants to make:")
print(changes.get_description())

proj.close()


# DEBUG CODE
#
# project_root = os.path.dirname(os.path.abspath(__file__))
#
# blob_src = open(os.path.join(project_root, "main", "blob.py")).read()
# test_src = open(os.path.join(project_root, "test", "test.py")).read()
#
# proj = project.Project(project_root)
#
# # Check what Rope resolves wl.count to in test.py
# test_resource = proj.get_resource("test/test.py")
# test_pymodule = proj.get_pymodule(test_resource)
#
# # Find the offset of 'count' in test.py
# offset = test_src.index("wl.count") + len("wl.")
# print(f"Offset of 'count' in test.py: {offset}")
#
# pyname = evaluate.eval_location(test_pymodule, offset)
# print(f"Rope resolves wl.count to: {pyname}")
# print(f"Type: {type(pyname)}")
#
#
# # Check WordList's superclasses
# blob_resource = proj.get_resource("main/blob.py")
# blob_pymodule = proj.get_pymodule(blob_resource)
# wordlist_pyclass = blob_pymodule["WordList"].get_object()
#
# print(f"WordList superclasses: {wordlist_pyclass.get_superclasses()}")
# print(f"WordList attributes: {list(wordlist_pyclass.get_attributes().keys())}")
#
#
# blob_resource = proj.get_resource("main/blob.py")
# blob_pymodule = proj.get_pymodule(blob_resource)
# wordlist_pyclass = blob_pymodule["WordList"].get_object()
#
# structural = wordlist_pyclass._get_structural_attributes()
# concluded = wordlist_pyclass._get_concluded_attributes()
#
# print(f"'count' in structural: {'count' in structural}")
# print(f"'count' in concluded: {'count' in concluded}")
# print(f"structural['count']: {structural.get('count')}")
# print(f"concluded['count']: {concluded.get('count')}")
#
#
# test_scope = test_pymodule.get_scope()
# inner_scope = test_scope.get_inner_scope_for_line(8)  # line with wl = tb.WordList(...)
# print(f"Scope kind: {inner_scope.get_kind()}")
# print(f"Names in scope: {list(inner_scope.get_names().keys())}")
#
# wl_pyname = inner_scope.get_names().get("wl")
# print(f"wl pyname: {wl_pyname}")
# if wl_pyname:
#     wl_obj = wl_pyname.get_object()
#     print(f"wl object: {wl_obj}")
#     print(f"wl type: {wl_obj.get_type()}")
#     print(f"wl type class: {type(wl_obj.get_type())}")
#
# print(f"wl type is BuiltinClass: {isinstance(wl_obj.get_type(), BuiltinClass)}")
#
#
# proj.close()