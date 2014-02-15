# Sublime RuboCop plugin
#
# Author: Patrick Derichs (patderichs@gmail.com)
# License: MIT (http://opensource.org/licenses/MIT)

import sublime
import sublime_plugin
import locale
import re
import os

if sublime.version() >= '3000':
  from RuboCop.file_tools import FileTools
  from RuboCop.rubocop_runner import RubocopRunner
  from RuboCop.constants import *
else:
  from file_tools import FileTools
  from rubocop_runner import RubocopRunner
  from constants import *

listener_instance = None

# Event listener to provide on the fly checks when saving a ruby file.
class RubocopEventListener(sublime_plugin.EventListener):
  def __init__(self):
    global listener_instance
    super(RubocopEventListener, self).__init__()
    self.file_remark_dict = {}
    listener_instance = self

  def get_current_file_dict(self, view):
    if not (view.file_name() in self.file_remark_dict.keys()):
      return None

    return self.file_remark_dict[view.file_name()]

  def clear_marks(self, view):
    dct = self.get_current_file_dict(view)
    if dct:
      dct.clear()
    view.erase_regions(REGIONS_ID)

  def line_no_of_cop_result(self, file_name, result):
    res = result.decode(locale.getpreferredencoding())
    reg_result = re.search(r"^([^:]+):([0-9]*):.*:(.*)", res)
    if reg_result:
      return reg_result.group(2), reg_result.group(3).strip()
    return None, None

  def set_marks_by_results(self, view, cop_results):
    lines = []
    path = view.file_name()
    base_file = os.path.basename(path)
    view_dict = self.get_current_file_dict(view)
    if not view_dict:
      view_dict = {}
      self.file_remark_dict[path] = view_dict
    for result in cop_results:
      line_no, message = self.line_no_of_cop_result(base_file, result)
      if line_no:
        ln = int(line_no) - 1
        view_dict[ln] = message
        line = view.line(view.text_point(ln, 0))
        lines.append(sublime.Region(line.begin(), line.end()))
    view.add_regions(REGIONS_ID, lines, 'invalid', 'circle', 
      sublime.PERSISTENT)

  def run_rubocop(self, path):
    s = sublime.load_settings(SETTINGS_FILE)
    use_rvm = s.get('check_for_rvm')
    use_rbenv = s.get('check_for_rbenv')
    cmd = s.get('rubocop_command')
    rvm_path = s.get('rvm_auto_ruby_path')
    rbenv_path = s.get('rbenv_path')
    runner = RubocopRunner(use_rbenv, use_rvm, cmd, rvm_path, rbenv_path)
    output = runner.run(path).splitlines()
    return output

  def mark_issues(self, view, mark):
    self.clear_marks(view)
    if mark:
      results = self.run_rubocop(view.file_name())
      self.set_marks_by_results(view, results)

  def do_in_file_check(self, view):
    if not FileTools.is_ruby_file(view.file_name()):
      return
    mark = sublime.load_settings(SETTINGS_FILE).get('mark_issues_in_view')
    self.mark_issues(view, mark)

  def on_post_save(self, view):
    if sublime.version() >= '3000':
      # To improve performance, we use the async method within ST3
      return

    self.do_in_file_check(view)

  def on_post_save_async(self, view):
    self.do_in_file_check(view)

  def on_load_async(self, view):
    self.do_in_file_check(view)

  def on_selection_modified(self, view):
    curr_sel = view.sel()
    if curr_sel:
      view_dict = self.get_current_file_dict(view)
      if not view_dict:
        return
      first_sel = curr_sel[0]
      row, col = view.rowcol(first_sel.begin())
      if row in view_dict.keys():
        sublime.status_message('RuboCop: {0}'.format(view_dict[row]))
      else:
        sublime.status_message('')
