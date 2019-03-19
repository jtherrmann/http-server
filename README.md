# HTTP server

Jake Herrmann\
CS 321 Spring 2019\
Operating Systems

## Contents

TODO

## Getting started

Known to work on Debian GNU/Linux 9 (stretch).

1. Install the `python3-pip` package.
2. Clone this repo and run `cd http-server`.
3. Run `pip3 install . --user`, which installs the `http_server` package to
`~/.local/` or to the location specified by `PYTHONUSERBASE`. (Also see the
docs for
[--user](https://pip.pypa.io/en/stable/reference/pip_install/#cmdoption-user)
and
[PYTHONUSERBASE](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUSERBASE).)
4. Run `python3 tests/` to run all of the tests. They should all pass. You can
also run `python3` on any individual `.py` file in `tests/` in order to run
only the tests from that file. Tests should always be run from the project's
root directory.
5. Run the server with `http-server`. You may need to first add `~/.local/bin`
or `$PYTHONUSERBASE/bin` to your `PATH`.

TODO: give brief description of what `http-server` script should do