# These are some unit tests for rubocop_runner (one of the main
# actors of that plugin). They are commented out since ST is 
# parsing that file on startup and it causes a lot of warnings
# in the ST console. I will comment that in as soon as we got
# a better location for that file or make ST ignore it.

# import unittest

# from rubocop_runner import RubocopRunner

# RVM_PATH = '/.rvm/bin/rvm-auto-ruby'
# RBENV_PATH = '/.rbenv/bin/rbenv'

# class RuboCopRunnerTests(unittest.TestCase):
#   def test_init_with_rbenv(self):
#     runner = RubocopRunner(True, False, 'abc')
#     self.assertTrue(runner.use_rbenv)
#     self.assertFalse(runner.use_rvm)
#     self.assertEqual(runner.custom_rubocop_cmd, 'abc')

#   def test_init_with_rvm(self):
#     runner = RubocopRunner(False, True, 'xyz')
#     self.assertFalse(runner.use_rbenv)
#     self.assertTrue(runner.use_rvm)
#     self.assertEqual(runner.custom_rubocop_cmd, 'xyz')

#   def test_load_cmd_prefix_rbenv(self):
#     runner = RubocopRunner(True, False, 'xyz')
#     prefix = runner.load_cmd_prefix()
#     self.assertTrue(runner.cmd_prefix.endswith(RBENV_PATH + ' exec'))

#   def test_load_cmd_prefix_rvm(self):
#     runner = RubocopRunner(False, True, 'xyz')
#     prefix = runner.load_cmd_prefix()
#     self.assertTrue(runner.cmd_prefix.endswith(RVM_PATH + ' -S'))

#   def test_load_cmd_prefix_no_prefix(self):
#     runner = RubocopRunner(False, False, '')
#     prefix = runner.load_cmd_prefix()
#     self.assertEqual(runner.cmd_prefix, '')

#   def test_load_rvm_use_rvm(self):
#     runner = RubocopRunner(False, True, '')
#     self.assertTrue(runner.load_rvm())

#   def test_load_rvm_not_using_rvm(self):
#     runner = RubocopRunner(True, False, '')
#     self.assertFalse(runner.load_rvm())

#   def test_load_rbenv_use_rbenv(self):
#     runner = RubocopRunner(True, False, '')
#     self.assertTrue(runner.load_rbenv())

#   def test_load_rbenv_not_using_rbenv(self):
#     runner = RubocopRunner(False, True, '')
#     self.assertFalse(runner.load_rbenv())

#   def test_command_list_rvm(self):
#     runner = RubocopRunner(False, True, '')
#     lst = runner.command_list()
#     self.assertEqual(len(lst), 3)
#     self.assertTrue(lst[0].endswith(RVM_PATH))
#     self.assertEqual(lst[1], '-S')
#     self.assertEqual(lst[2], 'rubocop')

#   def test_command_list_rbenv(self):
#     runner = RubocopRunner(True, False, '')
#     lst = runner.command_list()
#     self.assertEqual(len(lst), 3)
#     self.assertTrue(lst[0].endswith(RBENV_PATH))
#     self.assertEqual(lst[1], 'exec')
#     self.assertEqual(lst[2], 'rubocop')

#   def test_command_list_custom(self):
#     runner = RubocopRunner(False, False, '666')
#     self.assertEqual(runner.command_list(), ['666'])
    
#   # TODO: Test run method

# def main():
#   unittest.main()

# if __name__ == '__main__':
#   main()
