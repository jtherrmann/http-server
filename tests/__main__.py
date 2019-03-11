import os
import unittest


if __name__ == '__main__':
    tests_path = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.dirname(tests_path)
    if os.getcwd() != project_path:
        print(
            'Error: when running tests, your cwd must be the root of the '
            'project: {}'.format(project_path)
        )
    else:
        from test_server import ServerEchoTestCase, ServerTripleCapsTestCase  # noqa F401
        from test_requests import ParseTestCase  # noqa F401
        unittest.main()
