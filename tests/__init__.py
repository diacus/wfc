import json
import os
import sys
import unittest

from wfc import core
from wfc.cli import make_argument_parser

from unittest.mock import MagicMock
from tests.util import mixins


TESTS_HOME = os.path.abspath(os.path.dirname(__file__))
SAMPLES_HOME = os.path.join(TESTS_HOME, 'samples')


class CompilerTestCase(unittest.TestCase, mixins.TmpIOHandler):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.maxDiff = None
        self.arg_parser = make_argument_parser()
        self._sys_stderr = sys.stderr
        sys.stderr = self.open_tmpout()

    def tearDown(self):
        sys.stderr = self._sys_stderr
        self.unlink_tmpio()

    def _mock_output(self, context, tstin, tstout):
        context.get_input_file = MagicMock(name='get_input_file')
        context.get_output_file = MagicMock(name='get_output_file')
        context.get_input_file.return_value = tstin
        context.get_output_file.return_value = tstout

    def _compile_to_json(self, test_target):
        script = self._compile_sample('{}.flow'.format(test_target))
        self._prune_action_ids(script)

        expected_script = self._load_json_script('{}.json'.format(test_target))
        self.assertDictEqual(expected_script, script)

    def _compile_to_json_with_failure(self, test_target):
        with self.assertRaises(AssertionError):
            self._compile_sample('{}.flow'.format(test_target))

    def _compile_sample(self, sample_name):
        with self._load_sample(sample_name) as sample_script, \
                core.CompilerContext() as context:
            tmp_out = self.open_tmpout()
            self._mock_output(context, sample_script, tmp_out)
            rc = core.compile(context)
            tmp_out.close()

        output = self.open_tmpin().read()
        assert rc == 0, 'Compilation failed\n{}'.format(output)

        with self.open_tmpin() as compiled_sample:
            return json.load(compiled_sample)

    def _compile_with_args(self, args):
        with core.CompilerContext(self.arg_parser.parse_args(args)) as context:
            context.set_quiet()
            return core.compile(context)

    def _load_json_script(self, script_name):
        with self._load_sample(script_name) as script_file:
            return json.load(script_file)

    def _load_sample(self, sample_name):
        sample_path = os.path.join(SAMPLES_HOME, sample_name)
        return open(sample_path, 'r')

    def _prune_action_ids(self, script):
        for dialog in script['dialogs']:
            for action in dialog['actions']:
                action.pop('id')