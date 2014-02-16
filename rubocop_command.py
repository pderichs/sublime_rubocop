# Sublime RuboCop plugin
#
# Author: Patrick Derichs (patderichs@gmail.com)
# License: MIT (http://opensource.org/licenses/MIT)

import sublime_plugin
import sublime
import os
import tempfile

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
    use_rvm = s.get('check_for_rvm')
    use_rbenv = s.get('check_for_rbenv')
    self.rubocop_command = s.get('rubocop_command')
    rvm_auto_ruby_path = s.get('rvm_auto_ruby_path')
    rbenv_path = s.get('rbenv_path')

    self.runner = RubocopRunner(use_rbenv, use_rvm, self.rubocop_command, rvm_auto_ruby_path, rbenv_path)
    self.rubocop_command = self.runner.command_string() + ' {options} {path}'

  def used_options(self):
    return ''

  def command_with_options(self):
    return self.rubocop_command.replace('{options}', self.used_options())

  def run_rubocop_on(self, path, file_list=False):
    if not path:
      return

    if not file_list:
      # Single item to check.
      quoted_file_path = FileTools.quote(path)
      working_dir = os.path.dirname(quoted_file_path)
    else:
      # Multiple files to check.
      working_dir = '.'
      quoted_file_path = ''
      for file in path:
        quoted_file_path += FileTools.quote(file) + ' '

    cop_command = self.command_with_options()
    rubocop_cmd = cop_command.replace('{path}', quoted_file_path)

    self.run_shell_command(rubocop_cmd, working_dir)

  def run_shell_command(self, command, working_dir='.'):
    if not command:
      return

    self.view.window().run_command('exec', {
      'cmd': [command],
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
    view = self.view
    path = view.file_name()
    quoted_file_path = FileTools.quote(path)

    if view.is_read_only():
      sublime.message_dialog('RuboCop: Unable to run auto correction on a read only buffer.')
      return

    # Inform user about unsaved contents of current buffer
    cancel_op = False
    if view.is_dirty():
      warn_msg = 'RuboCop: The curent buffer is modified. Save the file and continue?'
      cancel_op = not sublime.ok_cancel_dialog(warn_msg)

    if cancel_op:
      return
    else:
      # Save the file
      view.run_command('save')

    # Copy the current file to a temp file
    content = view.substr(sublime.Region(0, view.size()))
    f = tempfile.NamedTemporaryFile()

    self.write_to_file(f, content, view)
    f.flush()

    # Run rubocop with auto-correction on temp file
    self.runner.run(f.name, '-a')

    # Read contents of file
    f.seek(0)
    content = self.read_from_file(f)

    # Overwrite buffer contents (without saving!)
    rgn = sublime.Region(0, view.size())
    view.replace(edit, rgn, content)

    # TempFile will be deleted here
    f.close()

    view.run_command('save')
    sublime.status_message('RuboCop: Auto correction done.')

  def write_to_file(self, f, content, view):
    if sublime.version() < '3000':
      f.write(content)
      return
    f.write(bytes(content, view.encoding()))

  def read_from_file(self, f):
    if sublime.version() < '3000':
      return f.read()
    return f.read().decode(view.encoding())

# Runs a check on the currently opened file.
class RubocopCheckSingleFileCommand(RubocopCommand):
  def run(self, edit):
    super(RubocopCheckSingleFileCommand, self).run(edit)
    file_path = self.view.file_name()
    self.run_rubocop_on(file_path)

# Runs a check on the currently opened project.
class RubocopCheckProjectCommand(RubocopCommand):
  def run(self, edit):
    super(RubocopCheckProjectCommand, self).run(edit)
    folders = self.view.window().folders()
    if len(folders) > 0:
      self.run_rubocop_on(folders[0])
    else:
      sublime.status_message('RuboCop: No project folder available.')

# Runs a check on the folder of the current file.
class RubocopCheckFileFolderCommand(RubocopCommand):
  def run(self, edit):
    super(RubocopCheckFileFolderCommand, self).run(edit)
    file_path = self.view.file_name()
    project_folder = os.path.dirname(file_path)
    self.run_rubocop_on(project_folder)

# Runs a check on all open files.
class RubocopCheckOpenFilesCommand(RubocopCommand):
  def run(self, edit):
    super(RubocopCheckOpenFilesCommand, self).run(edit)
    files = self.open_ruby_files()
    if len(files) > 0:
      self.run_rubocop_on(files, True)
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
    return '-l'

# Runs a check on the current project (only using lint cops)
class RubocopCheckProjectOnlyWithLintCopsCommand(RubocopCheckProjectCommand):
  def used_options(self):
    return '-l'

# Runs a check on the current project (only using lint cops)
class RubocopCheckFileFolderOnlyWithLintCopsCommand(RubocopCheckFileFolderCommand):
  def used_options(self):
    return '-l'

# Runs a check on all open files (only using lint cops)
class RubocopCheckOpenFilesOnlyWithLintCopsCommand(RubocopCheckOpenFilesCommand):
  def used_options(self):
    return '-l'

# --------- Rails Cops -------------

# Runs a check on the current file (Rails)
class RubocopCheckCurrentFileRailsCommand(RubocopCheckSingleFileCommand):
  def used_options(self):
    return '-R'

# Runs a check on the current project (Rails)
class RubocopCheckProjectRailsCommand(RubocopCheckProjectCommand):
  def used_options(self):
    return '-R'

# Runs a check on the current project (Rails)
class RubocopCheckFileFolderRailsCommand(RubocopCheckFileFolderCommand):
  def used_options(self):
    return '-R'

# Runs a check on all open files (Rails)
class RubocopCheckOpenFilesRailsCommand(RubocopCheckOpenFilesCommand):
  def used_options(self):
    return '-R'
