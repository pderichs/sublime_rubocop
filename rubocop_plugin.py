import sublime
import os

class RubocopPlugin:

  @staticmethod
  def on_windows():
    return sublime.platform() == 'windows'

  @staticmethod
  def is_st2():
    return int(sublime.version()) < 3000

  @staticmethod
  def is_st3():
    return int(sublime.version()) >= 3000

  @staticmethod
  def current_project_folder():
    if RubocopPlugin.is_st3():
      project = sublime.active_window().project_data()
      project_base_path = os.path.dirname(sublime.active_window().project_file_name() or '')
      if not (project is None):
        if 'folders' in project:
          folders = project['folders']
          if len(folders) > 0:
            first_folder = folders[0]
            if 'path' in first_folder:
              path = first_folder['path']
              return (path if os.path.isabs(path) else os.path.join(project_base_path, path)) or ''
    else:
      folders = sublime.active_window().folders()
      if (not (folders is None)) and (len(folders) > 0):
        return folders[0]
    return ''