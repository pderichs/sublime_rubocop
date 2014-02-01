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
  from RuboCop.rubocop_command import SETTINGS_FILE
else:
  from file_tools import FileTools
  from rubocop_runner import RubocopRunner
  from rubocop_command import SETTINGS_FILE

REGIONS_ID = 'rubocop_remark_regions'

# Event listener to provide on the fly checks when saving a ruby file.
class RubocopEventListener(sublime_plugin.EventListener):
  def __init__(self):
    super(RubocopEventListener, self).__init__()
    self.remark_dict = {}

  def clear_marks(self, view):
    self.remark_dict = {}
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
    for result in cop_results:
      line_no, message = self.line_no_of_cop_result(base_file, result)
      if line_no:
        ln = int(line_no) - 1
        self.remark_dict[ln] = message
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

  def do_in_file_check(self, view):
    self.clear_marks(view)
    if not sublime.load_settings(SETTINGS_FILE).get('mark_issues_in_view'):
      return
    if not FileTools.is_ruby_file(view.file_name()):
      return
    results = self.run_rubocop(view.file_name())
    self.set_marks_by_results(view, results)

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
      first_sel = curr_sel[0]
      row, col = view.rowcol(first_sel.begin())
      if row in self.remark_dict.keys():
        sublime.status_message('RuboCop: {0}'.format(self.remark_dict[row]))
      else:
        sublime.status_message('')
