# Sublime RuboCop

A [Sublime Text](http://www.sublimetext.com/) plugin that runs [RuboCop](https://github.com/bbatsov/rubocop) on your Ruby files in the editor. It will mark issues right inside the view but it can also be called as a "compiler" from the ST menu.

The Plugin currently supports both ST2 and ST3, but the usage of ST3 is strongly recommended.

## Installation

### Prerequisites

Please make sure `rubocop` is installed:

`gem install rubocop`

### Recommended:

Install Sublime RuboCop via [Package Control](http://wbond.net/sublime_packages/package_control).

### Manual:

1. Navigate to the Sublime Text Packages folder (You can find the location of the Packages folder [here](http://docs.sublimetext.info/en/latest/basic_concepts.html#the-data-directory)).

2. Run the git clone command right inside the packages directory: `git clone git@github.com:pderichs/sublime_rubocop.git "RuboCop"`

3. Restart Sublime Text.

## What can it do for you?

By default, the plugin marks RuboCop issues right in the view when you open or save a Ruby file. Additionally you can run RuboCop from the ST menu in many ways. For example you can perform a RuboCop check on all files of the current project to get a general overview. The issues will be listed inside the Sublime output window, so you can easily navigate to each of them.

### ST2

Due to performance issues the plugin behaves a bit different under ST2. It will run RuboCop only when you **save** files. If you experience any performance issues when saving ruby files caused by that plugin, just disable the functionality in the settings (see ```mark_issues_in_view```).

## Environment

By default this plugin uses [rvm](https://rvm.io/) to run RuboCop, but you can switch to [rbenv](https://github.com/sstephenson/rbenv) or provide your own command line in the settings. The plugin uses default paths to run rvm or rbenv but you can customize these paths in the settings.

## ToDo

* The plugin has been tested within MacOS and Linux, but it has many issues on Windows.

## Credits

Thanks go out to [Will Bond](https://github.com/wbond) for his awesome sample and documentation about ST2 plugins, and thanks go out to the people implementing the [sublime-text-2-ruby-tests Plugin](https://github.com/maltize/sublime-text-2-ruby-tests) - your source gave me some important hints for my implementation.

## License

All of Sublime RuboCop is licensed under the MIT license.

  Copyright (c) 2013 Patrick Derichs <patderichs@gmail.com>

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.
