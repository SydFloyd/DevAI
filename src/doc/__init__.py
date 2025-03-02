from src.doc.auto_docstring import DocstringUpdater
from src.doc.auto_document import update_documentation

def auto_doc(project_root, update_file_docstrings=False, doc_output_path="docs.md"):
    if update_file_docstrings:
        updater = DocstringUpdater()
        updater.update_docstrings_in_directory(project_root)
    docs_path = update_documentation(project_root, doc_output_path)
    return docs_path