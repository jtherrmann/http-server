import os

import setuptools


setuptools.setup(
    name='http_server',
    packages=['http_server'],
    scripts=[os.path.join('scripts', 'run-server')],
    install_requires=['attrs>=18.2.0'],
    python_requires='>=3.5.3'
)
