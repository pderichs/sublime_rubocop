# A simple Sublime Text 2 Rubocop Plug-In.
#
# Author: Patrick Derichs (patderichs@gmail.com)
# License: MIT (http://opensource.org/licenses/MIT)

 
import sublime
import sublime_plugin
import os

class RubocopCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.file_path = self.view.file_name()
    self.check_file()
         
  def check_file(self):
    # Using rvm to run rubocop
    rvm_cmd = os.path.expanduser('~/.rvm/bin/rvm-auto-ruby')
    rubocop_cmd = rvm_cmd + ' -S rubocop ' + self.file_path

    self.run_shell_command(rubocop_cmd, '.')
     
  def run_shell_command(self, command, working_dir):
    if not command:
      return
    
    self.view.window().run_command("exec", {
      "cmd": [command],
      "shell": True,
      "working_dir": working_dir,
      "file_regex": r"^== (.*) ==",
      "line_regex": r"^.:\ ?([0-9]*): (.*)"
    })