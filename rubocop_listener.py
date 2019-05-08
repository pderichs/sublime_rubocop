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

# Event listener to provide on the fly checks when saving a ruby file.
class RubocopEventListener(sublime_plugin.EventListener):
  listener_instance = None

  def __init__(self):
    super(RubocopEventListener, self).__init__()
    self.file_remark_dict = {}
    RubocopEventListener.listener_instance = self
    if sublime.version() >= '3000':
      sublime.set_timeout_async(self.update_marks, 2)

  @classmethod
  def instance(cls):
    return cls.listener_instance

  def get_current_file_dict(self, view):
    if not (view.file_name() in self.file_remark_dict.keys()):
      return None

    return self.file_remark_dict[view.file_name()]

  def clear_marks(self, view):
    dct = self.get_current_file_dict(view)
    if dct:
      dct.clear()
    view.erase_regions(REGIONS_ID)

  def update_marks(self):
    for wnd in sublime.windows():
      for vw in wnd.views():
        self.do_in_file_check(vw)

  def line_no_of_cop_result(self, file_name, result):
    res = result.decode(locale.getpreferredencoding())
    reg_result = re.search(r"^.*:(\d*):\d*: .: (.*)$", res)
    if reg_result:
      return reg_result.group(1), reg_result.group(2).strip()
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
      if line_no is not None:
        ln = int(line_no) - 1
        view_dict[ln] = message
        line = view.line(view.text_point(ln, 0))
        lines.append(sublime.Region(line.begin(), line.end()))
    self.mark_lines(view, lines)

  def mark_lines(self, view, lines):
    s = sublime.load_settings(SETTINGS_FILE)
    icon = s.get('mark_icon') or 'arrow_right'
    view.add_regions(REGIONS_ID, lines, 'keyword', icon,
        REGIONS_OPTIONS_BITS)

  def run_rubocop(self, view):
    s = sublime.load_settings(SETTINGS_FILE)

    rubocop_disable = view.settings().get(
      'rubocop_disable',
      s.get('rubocop_disable'),
    )

    if rubocop_disable:
      return []


    use_rvm = view.settings().get('check_for_rvm', s.get('check_for_rvm'))
    use_rbenv = view.settings().get('check_for_rbenv', s.get('check_for_rbenv'))
    cmd = view.settings().get('rubocop_command', s.get('rubocop_command'))
    rvm_path = view.settings().get('rvm_auto_ruby_path', s.get('rvm_auto_ruby_path'))
    rbenv_path = view.settings().get('rbenv_path', s.get('rbenv_path'))
    cfg_file = view.settings().get('rubocop_config_file', s.get('rubocop_config_file'))
    chdir = view.settings().get('rubocop_chdir', s.get('rubocop_chdir'))

    if cfg_file:
      cfg_file = FileTools.quote(cfg_file)

    runner = RubocopRunner(
      {
        'use_rbenv': use_rbenv,
        'use_rvm': use_rvm,
        'custom_rubocop_cmd': cmd,
        'rvm_auto_ruby_path': rvm_path,
        'rbenv_path': rbenv_path,
        'on_windows': sublime.platform() == 'windows',
        'rubocop_config_file': cfg_file,
        'chdir': chdir,
        'is_st2': sublime.version() < '3000'
      }
    )
    output = runner.run([view.file_name()], ['--format', 'emacs', '--force-exclusion']).splitlines()

    return output

  def mark_issues(self, view, mark):
    self.clear_marks(view)
    if mark:
      results = self.run_rubocop(view)
      self.set_marks_by_results(view, results)

  def do_in_file_check(self, view):
    if not FileTools.is_ruby_file(view):
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
        view.set_status('rubocop', 'RuboCop: {0}'.format(view_dict[row]))
      else:
        view.set_status('rubocop', '')
