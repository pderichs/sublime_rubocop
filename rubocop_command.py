import sublime_plugin
import sublime
import os
import locale

if sublime.version() >= '3000':
  from RuboCop.file_tools import FileTools
  from RuboCop.rubocop_runner import RubocopRunner
  from RuboCop.constants import *
  from RuboCop.rubocop_listener import RubocopEventListener
else:
  from file_tools import FileTools
  from rubocop_runner import RubocopRunner
  from constants import *
  from rubocop_listener import RubocopEventListener

# Base class for all RuboCop commands
class RubocopCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.load_config()

  def load_config(self):
    s = sublime.load_settings(SETTINGS_FILE)
    cfg_file = s.get('rubocop_config_file')
    if cfg_file:
      cfg_file = FileTools.quote(cfg_file)
    self.runner = RubocopRunner(
      {
        'use_rbenv': s.get('check_for_rbenv'),
        'use_rvm': s.get('check_for_rvm'),
        'custom_rubocop_cmd': s.get('rubocop_command'),
        'rvm_auto_ruby_path': s.get('rvm_auto_ruby_path'),
        'rbenv_path': s.get('rbenv_path'),
        'on_windows': (sublime.platform() == 'windows'),
        'rubocop_config_file': cfg_file
      }
    )

  def used_options(self):
    return []

  def run_rubocop_on(self, pathlist):
    if len(pathlist) == 0:
      return

    working_dir = ''
    if len(pathlist) >= 1:
      working_dir = os.path.dirname(pathlist[0])
      if sublime.platform() == 'windows':
        working_dir = working_dir.replace('\\', '/')
      print("Working Dir: " + working_dir)

    quoted_paths = []
    for path in pathlist:
      quoted_paths.append(FileTools.quote(path))

    rubocop_cmd = self.runner.command_list(
      quoted_paths,
      self.used_options()
    )
    self.run_shell_command(rubocop_cmd, working_dir)

  def run_shell_command(self, command, working_dir='.'):
    self.view.window().run_command('exec', {
      'cmd': command,
      'shell': True,
      'working_dir': working_dir,
      'file_regex': r"^([^:]+):([0-9]*)",
    })

# --------- General rubocop commands -------------

# Toggles mark_issues_in_view setting
class RubocopPauseToggleCommand(RubocopCommand):
  def run(self, edit):
    super(RubocopPauseToggleCommand, self).run(edit)
    self.pause()

  def pause(self):
    s = sublime.load_settings(SETTINGS_FILE)
    mark_issues_in_view = s.get('mark_issues_in_view')
    s.set('mark_issues_in_view', not mark_issues_in_view)
    sublime.save_settings(SETTINGS_FILE)
    RubocopEventListener.instance().update_marks()

# Calling autocorrect on the current file
class RubocopAutoCorrectCommand(RubocopCommand):
  def run(self, edit):
    super(RubocopAutoCorrectCommand, self).run(edit)

    cancel_op = self.user_wants_to_cancel()
    if cancel_op:
      return

    view = self.view
    path = view.file_name()
    quoted_file_path = FileTools.quote(path)

    if view.is_read_only():
      sublime.message_dialog('RuboCop: Unable to run auto correction on a read only buffer.')
      return

    # Inform user about unsaved contents of current buffer
    if view.is_dirty():
      warn_msg = 'RuboCop: The curent buffer is modified. Save the file and continue?'
      cancel_op = not sublime.ok_cancel_dialog(warn_msg)

    if cancel_op:
      return
    else:
      view.run_command('save')

    RubocopEventListener.instance().clear_marks(view)

    quoted_file_path = FileTools.quote(path)

    # Run rubocop with auto-correction
    self.runner.run([quoted_file_path], ['-a'])

    sublime.status_message('RuboCop: Auto correction done.')

  def user_wants_to_cancel(self):
    s = sublime.load_settings(SETTINGS_FILE)
    show_warning = s.get('show_auto_correct_warning')
    if not show_warning:
      return False

    return not sublime.ok_cancel_dialog("""
Attention! You are about to run auto correction on the current file.

The contents of the current file will be modified/overwritten by RuboCop.

Do you want to continue?

(You can disable this warning message in the settings.)
      """)

  def write_to_file(self, f, content, view):
    if sublime.version() < '3000':
      f.write(content)
      return
    f.write(bytes(content, view.encoding()))

  def read_from_file(self, f, view):
    if sublime.version() < '3000':
      return f.read()
    return f.read().decode(view.encoding())

# Runs a check on the currently opened file.
class RubocopCheckSingleFileCommand(RubocopCommand):
  def run(self, edit):
    super(RubocopCheckSingleFileCommand, self).run(edit)
    file_path = self.view.file_name()
    self.run_rubocop_on([file_path])

# Runs a check on the currently opened project.
class RubocopCheckProjectCommand(RubocopCommand):
  def run(self, edit):
    super(RubocopCheckProjectCommand, self).run(edit)
    folders = self.view.window().folders()
    if len(folders) > 0:
      self.run_rubocop_on([folders[0]])
    else:
      sublime.status_message('RuboCop: No project folder available.')

# Runs a check on the folder of the current file.
class RubocopCheckFileFolderCommand(RubocopCommand):
  def run(self, edit):
    super(RubocopCheckFileFolderCommand, self).run(edit)
    file_path = self.view.file_name()
    project_folder = os.path.dirname(file_path)
    self.run_rubocop_on([project_folder])

# Runs a check on all open files.
class RubocopCheckOpenFilesCommand(RubocopCommand):
  def run(self, edit):
    super(RubocopCheckOpenFilesCommand, self).run(edit)
    files = self.open_ruby_files()
    if len(files) > 0:
      self.run_rubocop_on(files)
    else:
      sublime.status_message('RuboCop: There are no Ruby files to check.')

  def open_ruby_files(self):
    files = []
    views = self.view.window().views()
    for vw in views:
      file_path = vw.file_name()
      if FileTools.is_ruby_file(file_path):
        files.append(file_path)
    return files


# --------- Lint Cops -------------

# Runs a check on the current file (only using lint cops)
class RubocopCheckCurrentFileOnlyWithLintCopsCommand(RubocopCheckSingleFileCommand):
  def used_options(self):
    return ['-l']

# Runs a check on the current project (only using lint cops)
class RubocopCheckProjectOnlyWithLintCopsCommand(RubocopCheckProjectCommand):
  def used_options(self):
    return ['-l']

# Runs a check on the current project (only using lint cops)
class RubocopCheckFileFolderOnlyWithLintCopsCommand(RubocopCheckFileFolderCommand):
  def used_options(self):
    return ['-l']

# Runs a check on all open files (only using lint cops)
class RubocopCheckOpenFilesOnlyWithLintCopsCommand(RubocopCheckOpenFilesCommand):
  def used_options(self):
    return ['-l']

# --------- Rails Cops -------------

# Runs a check on the current file (Rails)
class RubocopCheckCurrentFileRailsCommand(RubocopCheckSingleFileCommand):
  def used_options(self):
    return ['-R']

# Runs a check on the current project (Rails)
class RubocopCheckProjectRailsCommand(RubocopCheckProjectCommand):
  def used_options(self):
    return ['-R']

# Runs a check on the current project (Rails)
class RubocopCheckFileFolderRailsCommand(RubocopCheckFileFolderCommand):
  def used_options(self):
    return ['-R']

# Runs a check on all open files (Rails)
class RubocopCheckOpenFilesRailsCommand(RubocopCheckOpenFilesCommand):
  def used_options(self):
    return ['-R']

# Opens all offensive files in the current project
class RubocopOpenAllOffensiveFilesCommand(RubocopCommand):
  def run(self, edit):
    super(RubocopOpenAllOffensiveFilesCommand, self).run(edit)

    folders = self.view.window().folders()
    if len(folders) <= 0:
      sublime.status_message('RuboCop: No project folder available.')
      return

    folder = FileTools.quote(folders[0])

    # Run rubocop with file formatter
    file_list = self.runner.run([folder], ['--format files']).splitlines()

    for path in file_list:
      self.view.window().open_file(path.decode(locale.getpreferredencoding()))

    sublime.status_message('RuboCop: Opened ' + str(len(file_list)) + ' files.')

# Shows the offense count by type
class RubocopProjectOffenseCountCommand(RubocopCheckProjectCommand):
  def used_options(self):
    return ['--format', 'offenses']
