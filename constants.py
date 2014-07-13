import sublime

REGIONS_ID = 'rubocop_remark_regions'
SETTINGS_FILE = 'RuboCop.sublime-settings'
REGIONS_OPTIONS_BITS = (sublime.DRAW_EMPTY |
                       sublime.DRAW_OUTLINED |
                       sublime.HIDE_ON_MINIMAP)
if int(sublime.version()) >= 3000:
  REGIONS_OPTIONS_BITS = (sublime.DRAW_EMPTY |
                         sublime.DRAW_NO_FILL |
                         sublime.DRAW_NO_OUTLINE |
                         sublime.DRAW_SQUIGGLY_UNDERLINE |
                         sublime.HIDE_ON_MINIMAP)
