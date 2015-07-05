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
  def is_ruby_file(view):
    if not view:
      return False
    syntax_file = view.settings().get('syntax')
    return syntax_file.endswith('Ruby.tmLanguage') or syntax_file.endswith('Ruby on Rails.tmLanguage')
