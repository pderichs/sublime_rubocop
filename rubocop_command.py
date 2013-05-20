# A simple Sublime Text 2 Rubocop Plug-In.
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
      self.rubocop_command = 'rubocop {path}'

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

  def run_rubocop_on(self, path):
    if not path:
      return

    # TODO: Use shlex.quote as soon as a newer python version is available.
    quoted_file_path = pipes.quote(path)
    rubocop_cmd = self.cmd_prefix + ' ' + self.rubocop_command.replace(
      '{path}', quoted_file_path)
    
    working_dir = os.path.dirname(quoted_file_path)

    self.run_shell_command(rubocop_cmd, working_dir)

  def run_shell_command(self, command, working_dir='.'):
    if not command:
      return
    
    self.view.window().run_command('exec', {
      'cmd': [command],
      'shell': True,
      'working_dir': working_dir,
      'file_regex': r"^== (.*) ==",
      'line_regex': r"^.:\ *([0-9]*): (.*)"
    })

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
