import re
import logging


class RedactingFilter(logging.Filter):
    # Do not try and redact the built in values. With the wrong regex it can break the logging
    ignore_keys = {
        'name', 'levelname', 'levelno', 'pathname', 'filename', 'module',
        'exc_info', 'exc_text', 'stack_info', 'lineno', 'funcName', 'created',
        'msecs', 'relativeCreated', 'thread', 'threadName', 'process',
        'processName', 'args',
    }

    def __init__(self, patterns, default_mask='****', mask_keys=None):
        if mask_keys is None:
            mask_keys = {}
        super(RedactingFilter, self).__init__()
        self._patterns = patterns
        self._default_mask = str(default_mask)
        self._mask_keys = set(mask_keys)

    def filter(self, record):
        d = vars(record)
        for k, content in d.items():
            if k not in self.ignore_keys:
                d[k] = self.redact(content, k)

        # Also clean any contents in args
        if isinstance(record.args, dict):
            for k in record.args.keys():
                record.args[k] = self.redact(record.args[k], k)
        else:
            record.args = tuple(self.redact(arg) for arg in record.args)

        return True

    def redact(self, content, key=None):
        if content:
            if isinstance(content, dict):
                for k, v in content.items():
                    content[k] = self.redact(v)

            elif isinstance(content, (list, tuple)):
                for i, v in enumerate(content):
                    content[i] = self.redact(v)

            elif key in self._mask_keys:
                content = self._default_mask

            else:
                content = isinstance(content, str) and content or str(content)
                for pattern in self._patterns:
                    content = re.sub(pattern, self._default_mask, content)

        return content
