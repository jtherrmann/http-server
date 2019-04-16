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
2. Clone this repo with `git clone --recurse-submodules <url>` and then run `cd
http-server`.
3. Run `pip3 install . --user`, which installs the `http_server` package to
`~/.local/` or to the location specified by `PYTHONUSERBASE`. (Also see the
docs for
[--user](https://pip.pypa.io/en/stable/reference/pip_install/#cmdoption-user)
and
[PYTHONUSERBASE](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONUSERBASE).)
4. Run `./run-tests`. All tests should pass. Tests should always be run from
the project's root directory.
5. Run `which jth-default-server`. If `jth-default-server` is not found, try
adding `~/.local/bin` (or `$PYTHONUSERBASE/bin`) to your `PATH`, then try
again.

## Default server

`http_server` provides a default server that translates URIs to filesystem
paths relative to the directory from which the server was run. `cd` to any
directory and run `jth-default-server`. The server is now available at
[http://localhost:8080/](http://localhost:8080/).

### *Pong* demo

This project includes a submodule for [Jake Gordon's
javascript-pong](https://github.com/jakesgordon/javascript-pong). From this
project's root directory, run `cd javascript-pong` and then run
`jth-default-server`. Go to
[http://localhost:8080/index.html](http://localhost:8080/index.html), enable
the `sound` option, and press `1` to start a single-player game.

Note that I did not write any of the *Pong* code, but I had to make sure my
server could serve HTML, CSS, JavaScript, images, and audio files in order to
host *Pong*. Go to [http://localhost:8080/](http://localhost:8080/) in order to
browse the files contained in the *Pong* project. In particular, navigate to
[http://localhost:8080/images](http://localhost:8080/images) and
[http://localhost:8080/sounds](http://localhost:8080/sounds) and observe that
the server successfully responds with the contents of requested images and
audio files.

## Dynamic CSS server

`http_server` also provides a server that translates URIs to CSS. Run
`jth-dynamic-css-server` and go to
[http://localhost:8080/](http://localhost:8080/) for further instructions.

## Custom request handlers

The only difference between the default server and the dynamic CSS server is
the handler function passed to `run_server`. You can define your own handler
function (and wrap it with the `create_handler` decorator) in order to specify
how your server responds to requests.

For example, here is a simple script for running a server that echoes the
requested URI back to the client:

```python
#!/usr/bin/env python3

from http_server.handlers import create_handler
from http_server.media_types import media_types
from http_server.requests import Request
from http_server.responses import Response
from http_server.server import run_server


@create_handler  # Wrap our handler using the create_handler decorator.
def echo_handler(request: Request) -> Response:
    message_body = 'You requested URI /{}. Here it is.'.format(
        '/'.join(request.uri)
    )
    return Response(200, media_types['plain'], message_body)


if __name__ == '__main__':
    # Run a TCP server that uses our custom handler.
    run_server(echo_handler, verbose=True)
```

Also see the [jth-default-server](scripts/jth-default-server) and
[jth-dynamic-css-server](scripts/jth-dynamic-css-server) scripts.

## Security implications

There is a known security flaw in
[jth-default-server](scripts/jth-default-server). `default_handler` does not
remove `..` components from the request URI, which means that an attacker can
escape the directory from which the server was run. For example, you can
request `/..` to get the contents of the parent directory, or chain together an
arbitrary number of `/..` to eventually reach the filesystem's root directory,
and then get the contents of any directory or file for which the server has
read access.

It seems that many browsers automatically remove `..` components from URIs, so
this vulnerability may not be obvious if you're developing a server and only
testing it using a browser. In order to test this problem at the command line,
run `jth-default-server` from any directory and then run `jth-http-client` in a
separate terminal. The client script prompts you for URIs to request from the
server and prints the server's responses, so that you can request URIs
containing `..` components without interference from the browser.

I anticipated this vulnerability early on, but I decided to leave it in so that
I could use it to demonstrate the security implications of neglecting to
properly sanitize user input. The fix would be to simply modify the handler
function to remove any `..` components from request URIs.
