from tests import CompilerTestCase


class TestCallFunction(CompilerTestCase):
    def test_call_function_success(self):
        self._compile('call-function')

    def test_call_function_with_arguments(self):
        self._compile('call-function-with-arguments')

    def test_call_function_with_bad_syntax(self):
        self._compile_with_failure('call-function-bad-syntax')
