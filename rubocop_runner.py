import os
import subprocess
from file_tools import FileTools

RVM_PATH = '~/.rvm/bin/rvm-auto-ruby'
RBENV_PATH = '~/.rbenv/bin/rbenv'

class RubocopRunner(object):
  """This class takes care of the rubocop location and its execution"""
  def __init__(self, use_rbenv, use_rvm, custom_rubocop_cmd):
    self.use_rvm = use_rvm
    self.use_rbenv = use_rbenv
    self.custom_rubocop_cmd = custom_rubocop_cmd

  def load_cmd_prefix(self):
    self.cmd_prefix = ''
    if not self.load_rvm():
      self.load_rbenv()

  def load_rvm(self):
    rvm_cmd = os.path.expanduser(RVM_PATH)
    if FileTools.is_executable(rvm_cmd):
      self.cmd_prefix = rvm_cmd + ' -S'
      return True
    return False

  def load_rbenv(self):
    rbenv_cmd = os.path.expanduser(RBENV_PATH)
    if FileTools.is_executable(rbenv_cmd):
      self.cmd_prefix = rbenv_cmd + ' exec'
      return True
    return False
    
  def run(self, path, options=''):
    call_list = self.command_list()
    call_list.extend(options.split())
    call_list.extend(path.split())

    # print "--- Runner: Rubocop has started ---"
    # print "Options: " + options
    # print "Path: " + path
    # print "Command: " + ' '.join(call_list)

    p = subprocess.Popen(call_list, 
      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    # print "Output:"
    # print out

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
