"""
Simple checkpoint tracking helper class with dictionary-like access.  This is
used for modular inputs to track their state between executions.
"""
from __future__ import unicode_literals

import json
import os
from copy import deepcopy
from datetime import datetime, timedelta
from logging import getLogger

from six.moves.urllib.parse import quote

logger = getLogger("cypresspoint.checkpoint")


def json_dt_converter(o):
    if isinstance(o, datetime):
        return o.__str__()


class ModInputCheckpoint(object):
    NotSet = object()

    def __init__(self, checkpoint_dir, input_name):
        self.checkpoint_dir = checkpoint_dir
        self.input_name = input_name
        self.filename = self._safe_filename(checkpoint_dir, input_name)
        self.dump_after_updates = 10
        self._data = None
        self.default_item = KeyError
        self.updates = 0
        self._last_dump = None

    def __del__(self):
        # XXX: Review this.  What are the rules about raising an exception in __del__; no guarantees
        if self.updates > 0:
            raise Exception("You forgot to dump the checkpoint data.   Changes not saved!")

    def _safe_filename(self, checkpoint_dir, input_name):
        input_name = input_name.replace("://", "__")
        input_name = quote(input_name, safe="")
        return os.path.join(checkpoint_dir, input_name + ".json")

    def load(self, default=None):
        # XXX:  Support pulling in old checksum data from backup, IF primary gets corrupted.
        #       Shouldn't happen as we attempt to create the file safely, but weird things happen.
        cp_filename = self.filename
        logger.debug("Loading checkpoint data from %s", cp_filename)
        try:
            with open(cp_filename) as fp:
                self._data = json.load(fp) or {}
        except (IOError, ValueError):
            # If you see this message logged frequently, then there's an issue.
            logger.warning("[%s] Unable to process checkpoint file '%s'.  "
                           "This is normal for a new input.  Starting from scratch.",
                           self.input_name, cp_filename)
            if default:
                self._data = default
            else:
                self._data = {}

    def dump_on_interval(self, delta):
        """ Dump to disk if interval has elapsed even if dump_after_updates
        hasn't been reached.  This is helpful for long-lived modular inputs.

        A dump will also occur the very first time this function is called.
        """
        # type: (timedelta)
        now = datetime.now()
        if self._last_dump:
            if self.updates == 0:
                return False
            age = now - self._last_dump
            if age < delta:
                return False
        self.dump(_now=now)
        return True

    def dump(self, _now=None):
        # Safely write out checkpoint data; this should avoid MOST common issues
        cp_filename = self.filename

        cp_filename_bk = cp_filename + ".bak"
        cp_filename_new = "{}.new-{}".format(cp_filename, os.getpid())
        try:
            with open(cp_filename_new, "w") as fp:
                # Indentation makes this human readable, with minimal overhead
                json.dump(self._data, fp, indent=2, default=json_dt_converter)
                cp_file_size = fp.tell()

            # Backup existing file (unless this is the first-time run)
            if os.path.isfile(cp_filename):
                # Remove old backup, if present
                if os.path.isfile(cp_filename_bk):
                    os.unlink(cp_filename_bk)
                # Move previous live file to "backup"
                os.rename(cp_filename, cp_filename_bk)

            # Move NEW checkpoint data (temporary file) into place
            os.rename(cp_filename_new, cp_filename)
            if self._data is not None:
                logger.info("Checkpoint data saved file=%s entries=%d bytes=%d",
                            cp_filename, len(self._data), cp_file_size)
        except Exception:
            logger.exception("[%s] Failure while writing out checkpoint data.  "
                             "State not saved.", self.input_name)
            logger.warning("[%s] Emergency dump of checkpoint data to log:\n%s",
                           self.input_name, json.dumps(self._data), default=json_dt_converter)
        self.updates = 0
        self._last_dump = _now or datetime.now()

    def __getitem__(self, item):
        try:
            return self._data[item]
        except KeyError:
            if isinstance(self.default_item, Exception):
                raise self.default_item(item)
            return deepcopy(self.default_item)

    def get(self, item, default=NotSet):
        try:
            return self._data[item]
        except KeyError:
            if default is self.NotSet:
                return deepcopy(self.default_item)
            else:
                return default

    def __setitem__(self, key, value):
        self._data[key] = value
        self.updates += 1
        if self.updates >= self.dump_after_updates:
            self.dump()

    def setdefault(self, key, default):
        if key not in self._data:
            self._data[key] = default
        return self._data[key]
