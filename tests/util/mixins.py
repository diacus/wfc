import os
import tempfile


class TmpIOHandler:
    def _open_tmpfile(self, mode):
        self._tmp_file = open(self.get_tmp_path(), mode)
        return self._tmp_file

    def _unlink_tmp_file(self):
        os.unlink(self._tmp_path)

    def close_tmpio(self):
        if hasattr(self, '_tmp_file'):
            self._tmp_file.close()

    def get_tmp_path(self):
        if not hasattr(self, '_tmp_path'):
            _, self._tmp_path = tempfile.mkstemp()
        return self._tmp_path

    def open_tmpin(self):
        return self._open_tmpfile('r')

    def open_tmpout(self):
        return self._open_tmpfile('w')

    def unlink_tmpio(self):
        if hasattr(self, '_tmp_file'):
            if not self._tmp_file.closed:
                self._tmp_file.close()
            self._unlink_tmp_file()
