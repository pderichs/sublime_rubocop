# A simple Sublime Text 2 Rubocop Plug-In.
#
# Author: Patrick Derichs (patderichs@gmail.com)
# License: MIT (http://opensource.org/licenses/MIT)
 
import sublime
import sublime_plugin
import os
import pipes

class RubocopCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.check_file(self.view.file_name())
         
  def check_file(self, file_path):
    # Using rvm to run rubocop
    rvm_cmd = os.path.expanduser('~/.rvm/bin/rvm-auto-ruby')

    # TODO: Use shlex.quote as soon as a newer python version is available.
    quoted_file_path = pipes.quote(file_path)
    rubocop_cmd = rvm_cmd + ' -S rubocop ' + quoted_file_path

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
