import os
import pipes
import sublime

if sublime.version() >= '3000':
  RUBY_SYNTAX_FILES = [
    'Ruby.sublime-syntax',
    'Ruby on Rails.sublime-syntax',
    'RSpec.sublime-syntax'
  ]
else:
  RUBY_SYNTAX_FILES = [
    'Ruby.tmLanguage',
    'Ruby on Rails.tmLanguage',
    'RSpec.tmLanguage'
  ]

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

    if syntax_file == None:
      return False

    for syntax in RUBY_SYNTAX_FILES:
      if syntax_file.endswith(syntax):
        return True

    return False
