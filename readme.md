# Sublime RuboCop

A Sublime Text 2 plugin that runs a [RuboCop](https://github.com/bbatsov/rubocop) check on the current file or the current project. By default it uses [RVM](https://rvm.io/) to run RuboCop, but you can switch to [rbenv](https://github.com/sstephenson/rbenv) or provide your own command line in the settings.

Enjoy!

## Installation

Preferred way:

Install Sublime RuboCop via [Package Control](http://wbond.net/sublime_packages/package_control).

Alternative way:

1. Navigate to the Sublime Text 2 Packages folder (on Mac OS X it can be found here: `$HOME/Library/Application Support/Sublime Text 2/Packages`, if you use another OS you can find the location of the Packages folder [here](http://docs.sublimetext.info/en/latest/basic_concepts.html#the-data-directory))

2. Run the git clone command right inside the packages directory: `git clone git@github.com:pderichs/sublime_rubocop.git`

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
