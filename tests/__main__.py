import os
import unittest


if __name__ == '__main__':
    # TODO: also check cwd when running individual test files
    tests_path = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.dirname(tests_path)
    if os.getcwd() != project_path:
        print(
            'Error: when running tests, your cwd must be the root of the '
            'project: {}'.format(project_path)
        )
    else:
        from test_server import ServerEchoTestCase, ServerTripleCapsTestCase  # noqa F401
        from test_requests import RequestsTestCase  # noqa F401
        from test_responses import ResponsesTestCase  # noqa F401
        from test_handlers import HandlersTestCase  # noqa F401
        unittest.main()
