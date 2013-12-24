# A simple Sublime Text RuboCop Plug-In.
#
# Author: Patrick Derichs (patderichs@gmail.com)
# License: MIT (http://opensource.org/licenses/MIT)
 
import sublime_plugin
import sublime
import pipes
import os

# Base class for all RuboCop commands
class RubocopCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.load_config()

  def load_config(self):
    s = sublime.load_settings('RuboCop.sublime-settings')

    self.load_cmd_prefix(s)

    self.rubocop_command = s.get('rubocop_command')
    if not self.rubocop_command or self.rubocop_command is '':
      self.rubocop_command = 'rubocop {options} {path}'

  def load_cmd_prefix(self, s):
    self.cmd_prefix = ''
    if not self.load_rvm(s):
      self.load_rbenv(s)

  def load_rvm(self, s):
    rvm_cmd = os.path.expanduser('~/.rvm/bin/rvm-auto-ruby')
    if s.get("check_for_rvm") and self.is_executable(rvm_cmd):
      self.cmd_prefix = rvm_cmd + ' -S'
      return True

    return False

  def load_rbenv(self, s):
    rbenv_cmd = os.path.expanduser('~/.rbenv/bin/rbenv')
    if s.get('check_for_rbenv') and self.is_executable(rbenv_cmd):
      self.cmd_prefix = rbenv_cmd + ' exec'
      return True

    return False

  def is_executable(self, path):
    return os.path.isfile(path) and os.access(path, os.X_OK)

  def quote(self, path):
    # TODO: Use shlex.quote as soon as a newer python version is available.
    return pipes.quote(path)

  def used_options(self):
    return ''

  def command_with_options(self):
    return self.rubocop_command.replace('{options}', self.used_options())

  def run_rubocop_on(self, path, file_list=False):
    if not path:
      return

    if not file_list:
      # Single item to check.
      quoted_file_path = self.quote(path)
      working_dir = os.path.dirname(quoted_file_path)
    else:
      # Multiple files to check.
      working_dir = '.'
      quoted_file_path = ''
      for file in path:
        quoted_file_path += self.quote(file) + ' '

    cop_command = self.command_with_options()
    rubocop_cmd = self.cmd_prefix + ' ' + cop_command.replace(
        '{path}', quoted_file_path)

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
      name, ext = os.path.splitext(file_path)
      if ext == '.rb':
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
