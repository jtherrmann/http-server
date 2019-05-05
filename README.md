# HTTP server

Jake Herrmann\
CS 321 Spring 2019\
Operating Systems

## Contents

- [Goals](#goals)
- [Getting started](#getting-started)
  - [Troubleshooting tests](#troubleshooting-tests)
- [Default server](#default-server)
  - [*Pong* demo](#pong-demo)
- [Dynamic CSS server](#dynamic-css-server)
- [Custom request handlers](#custom-request-handlers)
- [Security implications](#security-implications)
- [Why no parallelism?](#why-no-parallelism)
- [Lessons learned](#lessons-learned)

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

### Troubleshooting tests

If some or all of the tests in [test_server.py](tests/test_server.py) fail with
`ConnectionRefusedError` because the client sockets cannot connect to the test
servers, then it may be necessary to increase the sleep duration in the
`ServerTestCase._wait` method so that the clients do not attempt to connect to
the servers before the servers begin accepting connections.

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
from http_server.media_types import MEDIA_TYPES
from http_server.requests import Request
from http_server.responses import Response
from http_server.server import run_server


@create_handler  # Wrap our handler using the create_handler decorator.
def echo_handler(request: Request) -> Response:
    message_body = 'You requested URI /{}. Here it is.'.format(
        '/'.join(request.uri)
    )
    return Response(200, MEDIA_TYPES['plain'], message_body)


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

## Why no parallelism?

I considered adding parallelism to [server.py](http_server/server.py), so that
a separate thread would handle each connected socket, allowing multiple clients
to connect simultaneously. I have some experience with Python's
[threading](https://docs.python.org/3/library/threading.html) library and I
think it would be straightforward to add multithreading to this project.
However, I decided against it for a few reasons.

First, I still needed to work on serving HTML, CSS, JavaScript, images, etc. as
well as create some interactive demos, in order to meet my original project
goals. These were higher priorities than implementing parallelism.

Second, I didn't want to add parallelism if I couldn't accurately test it for
both correctness and performance gains. I wanted to run an experiment in which
several clients send requests to the server at one time, in order to confirm
that the server handles them simultaneously, and to measure the performance
improvement over the single-threaded approach. Unfortunately, my development
machine only has two cores, so I can't run such an experiment locally. I
sketched out plans for running the experiment using AWS Lambda and/or EC2, but
I ran out of time.

## Lessons learned

- The Unix sockets interface is surprisingly high-level. Even if I had used the
  C interface, I don't think I would have needed to actually understand
  networking at the level of the hardware. I'm surprised that the operating
  system comes with the ability to set up a TCP server with just a few system
  calls.
- HTTP really is just plain ASCII on top of (in this case) TCP. I think it's
  really cool that there's nothing more to it than that. On the other hand, I
  would have liked to delve more into low-level sockets programming.
  Implementing a lower-level protocol like TCP sounds like a fun project.
- Playing with processes is fun! Python has a very nice `subprocess` module for
  creating and communicating with other processes, and I had fun using it while
  writing tests that spawn test servers and then send requests to those
  servers. In particular, I learned more about how to communicate with other
  processes using signals and how to track down and terminate rogue processes
  (e.g. if you accidentally close the terminal while your server is still
  running).
- "Servers" and "clients" aren't necessarily singular, independent machines.
  They're just processes communicating via sockets. Previously, I was confused
  by certain uses of the term "server". For example, I installed an
  auto-completion package for my text editor that ran a server in the
  background, and I was always unclear on what exactly that meant. Was it a
  server on the internet? On my local machine? How was it communicating with my
  text editor? Now I realize it was likely just a separate process
  communicating with my text editor via sockets. Before learning about sockets,
  I viewed writing multi-process applications and handling inter-process
  communication as a difficult and mysterious task, while now it seems very
  approachable.
- Parsing is not a very interesting problem. Better to use someone else's
  parser if one is available, or use a parser generator. In this case, I'm sure
  there are HTTP-parsing modules available for Python (possibly in the standard
  library).
- Sometimes rapid prototyping is more important than complete test coverage. In
  particular, if I were to do this project again, I would initially just use a
  few of Python's string-manipulation functions (like `str.split` for splitting
  strings on whitespace) in place of a proper recursive-descent parser, and not
  worry about writing tests to make sure my parser recognizes every possible
  kind of bad request.
