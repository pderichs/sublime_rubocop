# Sublime RuboCop plugin
#
# Author: Patrick Derichs (patderichs@gmail.com)
# License: MIT (http://opensource.org/licenses/MIT)

import os
import subprocess
import sublime

if sublime.version() >= '3000':
  from RuboCop.file_tools import FileTools
else:
  from file_tools import FileTools

class RubocopRunner(object):
  """This class takes care of the rubocop location and its execution"""
  def __init__(self, use_rbenv, use_rvm, custom_rubocop_cmd, rvm_auto_ruby_path, rbenv_path):
    self.use_rvm = use_rvm
    self.use_rbenv = use_rbenv
    self.custom_rubocop_cmd = custom_rubocop_cmd
    self.rvm_auto_ruby_path = rvm_auto_ruby_path
    self.rbenv_path = rbenv_path

  def load_cmd_prefix(self):
    self.cmd_prefix = ''
    if not self.load_rvm():
      self.load_rbenv()

  def load_rvm(self):
    rvm_cmd = os.path.expanduser(self.rvm_auto_ruby_path)
    if FileTools.is_executable(rvm_cmd):
      self.cmd_prefix = rvm_cmd + ' -S'
      return True
    return False

  def load_rbenv(self):
    rbenv_cmd = os.path.expanduser(self.rbenv_path)
    if FileTools.is_executable(rbenv_cmd):
      self.cmd_prefix = rbenv_cmd + ' exec'
      return True
    return False

  def run(self, path, options=''):
    call_list = self.command_list()
    call_list.extend(options.split())
    call_list.extend(path.split())

    p = subprocess.Popen(call_list,
      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    return out

  def command_list(self):
    cmd = ''
    if not self.custom_rubocop_cmd or self.custom_rubocop_cmd is '':
      self.load_cmd_prefix()
      cmd = self.cmd_prefix + ' rubocop'
    else:
      cmd = self.custom_rubocop_cmd

    return cmd.split()

  def command_string(self):
    return ' '.join(self.command_list())
