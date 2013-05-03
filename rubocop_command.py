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
    # Using rvm to run rubocop
    self.rvm_cmd = os.path.expanduser('~/.rvm/bin/rvm-auto-ruby')

  def run_rubocop_on(self, path):
    if not path:
      return
      
    # TODO: Use shlex.quote as soon as a newer python version is available.
    quoted_file_path = pipes.quote(path)
    rubocop_cmd = self.rvm_cmd + ' -S rubocop ' + quoted_file_path

    self.run_shell_command(rubocop_cmd)

  def run_shell_command(self, command, working_dir='.'):
    if not command:
      return
    
    self.view.window().run_command("exec", {
      "cmd": [command],
      "shell": True,
      "working_dir": working_dir,
      "file_regex": r"^== (.*) ==",
      "line_regex": r"^.:\ *([0-9]*): (.*)"
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
      sublime.status_message("RuboCop: No project folder available.")

class RubocopCheckFileFolderCommand(RubocopCommand):
  def run(self, edit):
    super(RubocopCheckFileFolderCommand, self).run(edit)
    file_path = self.view.file_name()
    project_folder = os.path.dirname(file_path)
    self.run_rubocop_on(project_folder)