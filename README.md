# HTTP server

Jake Herrmann\
CS 321 Spring 2019\
Operating Systems

## Contents

TODO

## Goals

**Overall goal:** Write an HTTP server in Python.

**Detailed goals:**

- Be able to serve HTML, CSS, and JavaScript in order to host a simple website.
  - Implement only as much of [HTTP/1.1](https://tools.ietf.org/html/rfc2616)
    as is needed to meet this goal.
- Do not use any networking libraries other than `socket`. In particular, do
  not use `http`, `socketserver`, `urllib`, or any third-party networking
  libraries (e.g. `requests`).
- Document (roughly) how the sockets code might be written using C system
  calls.
- Provide as much test coverage as possible, while still being practical.

## Getting started

Known to work on Debian GNU/Linux 9 (stretch).

1. Install the `python3-pip` and `python3-setuptools` packages.
2. Clone this repo and run `cd http-server`.
3. Run `pip3 install . --user`, which installs the `http_server` package to
`~/.local/` or to the location specified by `PYTHONUSERBASE`. (Also see the
docs for
[--user](https://pip.pypa.io/en/stable/reference/pip_install/#cmdoption-user)
and
[PYTHONUSERBASE](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUSERBASE).)
4. Run `./run-tests`. All tests should pass. Tests should always be run from
the project's root directory.
5. Run the server with `http-server`. You may need to first add `~/.local/bin`
or `$PYTHONUSERBASE/bin` to your `PATH`.

The server is now available at `http://localhost:8080/`. Any request is met
with a plaintext response informing the client of the requested URI. For
example, navigating to `http://localhost:8080/hello/world` in a web browser
should display some message informing you that you requested URI
`/hello/world`.