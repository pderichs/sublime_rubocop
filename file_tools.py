import os
import pipes

class FileTools(object):
  """Simple file operations"""
  @staticmethod
  def is_executable(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)

  @staticmethod
  def quote(path):
    # TODO: Use shlex.quote as soon as a newer python version is available.
    return pipes.quote(path)

  @staticmethod
  def is_ruby_file(path):
    if not path:
      return False
    name, ext = os.path.splitext(path)
    if ext == '.rb':
      return True
    return False
