import os

import setuptools


setuptools.setup(
    name='http_server',
    packages=['http_server'],
    scripts=[os.path.join('scripts', 'run-server')],
    python_requires='>=3.5.3'
)
