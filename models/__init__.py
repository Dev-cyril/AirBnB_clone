#!/usr/bin/python3
"""initialization"""


from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
