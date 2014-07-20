# Sublime RuboCop plugin
#
# Initial Author: Patrick Derichs (patderichs@gmail.com)
# License: MIT (http://opensource.org/licenses/MIT)

import os
import subprocess

RVM_DEFAULT_PATH = '~/.rvm/bin/rvm-auto-ruby'
RBENV_DEFAULT_PATH = '~/.rbenv/bin/rbenv'

class RubocopRunner(object):
  """This class takes care of the rubocop location and its execution"""
  def __init__(self, *initial_data, **kwargs):
    self.set_default_paths()
    for dictionary in initial_data:
      for key in dictionary:
        setattr(self, key, dictionary[key])
    for key in kwargs:
      setattr(self, key, kwargs[key])

  def set_default_paths(self):
    self.rvm_auto_ruby_path = RVM_DEFAULT_PATH
    self.rbenv_path = RBENV_DEFAULT_PATH

  # def __init__(self, use_rbenv, use_rvm, custom_rubocop_cmd, rvm_auto_ruby_path=None, rbenv_path=None):
    # self.use_rvm = use_rvm
    # self.use_rbenv = use_rbenv
    # self.custom_rubocop_cmd = custom_rubocop_cmd

    # if rvm_auto_ruby_path is None:
    #   self.rvm_auto_ruby_path = RVM_DEFAULT_PATH
    # else:
    #   self.rvm_auto_ruby_path = rvm_auto_ruby_path

    # if rbenv_path is None:
    #   self.rbenv_path = RBENV_DEFAULT_PATH
    # else:
    #   self.rbenv_path = rbenv_path

  def load_cmd_prefix(self):
    self.cmd_prefix = ''
    if not self.load_rvm():
      self.load_rbenv()

  def load_rvm(self):
    if self.use_rvm:
      rvm_cmd = os.path.expanduser(self.rvm_auto_ruby_path)
      self.cmd_prefix = rvm_cmd + ' -S'
      return True
    return False

  def load_rbenv(self):
    if self.use_rbenv:
      rbenv_cmd = os.path.expanduser(self.rbenv_path)
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
    if not self.custom_rubocop_cmd or self.custom_rubocop_cmd is '':
      self.load_cmd_prefix()
      cmd = self.cmd_prefix + ' rubocop'
    else:
      cmd = self.custom_rubocop_cmd

    return cmd.split()

  def command_string(self):
    return ' '.join(self.command_list())
