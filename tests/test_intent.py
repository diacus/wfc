from tests import CompilerTestCase


class TestIntent(CompilerTestCase):
    def test_intent_success(self):
        self._compile_to_json('intent')

    def test_intent_with_bad_syntax(self):
        self._compile_to_json_with_failure('intent-bad-syntax')