# A simple Sublime Text 2 RuboCop Plug-In.
#
# Author: Patrick Derichs (patderichs@gmail.com)
# License: MIT (http://opensource.org/licenses/MIT)

import sublime_plugin
import sublime
import pipes
import os
import string
import re

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

  def quote(self, path):
    # TODO: Use shlex.quote as soon as a newer python version is available.
    return pipes.quote(path)

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

    rubocop_cmd = self.cmd_prefix + ' ' + self.rubocop_command.replace(
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

# Runs a check on the currently opened file.
class RubocopCheckSingleFileCommand(RubocopCommand):
  def run(self, edit):
    super(RubocopCheckSingleFileCommand, self).run(edit)
    file_path = self.view.file_name()
    self.run_rubocop_on(file_path)

# Runs a check on modified files
class RubocopCheckModified(RubocopCommand):
  def run(self, edit):
    super(RubocopCheckModified, self).run(edit)
    root = self.git_repository_root()
    files = [os.path.join(root, relative) for relative in self.added_or_modified_ruby_files()]
    if len(files) > 0:
      self.run_rubocop_on(files, True)
    else:
      sublime.status_message('RuboCop: There are no Ruby files to check.')

  def added_or_modified_ruby_files(self):
    output = os.popen("git status --porcelain").read()
    lines = string.split(output, '\n')
    files = [line for line in lines if self.is_ruby(line)]
    return [self.strip_git_status(file) for file in files if self.is_added_or_modified(file)]

  def git_repository_root(self):
    return os.popen('git rev-parse --show-toplevel').read().strip()

  def strip_git_status(self, line):
    match = re.match(r'^( *[^ ]+) +(.*)', line)
    if match:
      return match.group(2)
    else:
      return None

  def is_ruby(self, file):
    return re.search(r'\.rb$', file)

  def is_added_or_modified(self, file):
    return re.search(r'^ *[AM] +', file)

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
