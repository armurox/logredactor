import re
import pytest
import logging
import logredactor


@pytest.fixture
def logger_setup(request):
    def get_logger(filters):
        # Use the test functions name to get a unique logger for that test
        logger = logging.getLogger(request.node.name)
        logger.addFilter(
            logredactor.RedactingFilter(
                filters,
                default_mask='****',
                mask_keys={'phonenumber'}
            )
        )
        return logger

    return get_logger


def test_no_args(caplog, logger_setup):
    logger = logger_setup([re.compile(r'\d{2}')])
    logger.warning("foo12bar")
    assert caplog.records[0].message == "foo****bar"


def test_arg_tuple(caplog, logger_setup):
    logger = logger_setup([re.compile(r'\d{3}')])
    logger.warning("foo %s-%s", '123', '4567')
    assert caplog.records[0].message == "foo ****-****7"


def test_arg_dict(caplog, logger_setup):
    logger = logger_setup([re.compile(r'\d{3}')])
    logger.warning("foo %(bar)s", {'bar': '123'})
    assert caplog.records[0].message == "foo ****"


def test_arg_dict_with_key_to_remove(caplog, logger_setup):
    logger = logger_setup([re.compile(r'\d{3}')])
    logger.warning("foo %s", {'phonenumber': '123'})
    assert caplog.records[0].message == "foo {'phonenumber': '****'}"


def test_extra_string_value(caplog, logger_setup):
    logger = logger_setup([re.compile(r'\d{3}')])
    logger.warning("foo", extra={'bar': '123 too'})
    assert caplog.records[0].bar == "**** too"


def test_extra_int_value(caplog, logger_setup):
    logger = logger_setup([re.compile(r'\d{3}')])
    logger.warning("foo", extra={'bar': 123})
    assert caplog.records[0].bar == "****"


def test_extra_float_value(caplog, logger_setup):
    logger = logger_setup([re.compile(r'\d{3}')])
    logger.warning("foo", extra={'bar': 123.6})
    assert caplog.records[0].bar == "****.6"


def test_extra_nested_dict(caplog, logger_setup):
    logger = logger_setup([re.compile(r'\d{3}')])
    extra_data = {
        'bar': {
            'api_key': 'key=123',
        },
    }
    logger.warning("foo", extra=extra_data)
    assert caplog.records[0].bar['api_key'] == "key=****"


def test_extra_do_not_redact_key(caplog, logger_setup):
    logger = logger_setup([re.compile(r'\d{3}')])
    logger.warning("foo", extra={'thing987': 'foobar'})
    assert caplog.records[0].thing987 == "foobar"


def test_extra_nested_dict_with_list(caplog, logger_setup):
    logger = logger_setup([re.compile(r'\d{3}')])
    extra_data = {
        'bar': {
            'thing': ['one', '456'],
        },
    }
    logger.warning("foo", extra=extra_data)
    assert caplog.records[0].bar['thing'][0] == 'one'
    assert caplog.records[0].bar['thing'][1] == '****'


def test_match_group(caplog, logger_setup):
    # Nothing in the code has to change
    # But this shows the use of a Positive Lookbehind
    # https://www.regextutorial.org/positive-and-negative-lookbehind-assertions.php
    logger = logger_setup([re.compile(r'(?<=api_key=)[\w-]+')])
    logger.warning("example.com?api_key=this-is-my-key&sort=price")
    assert caplog.records[0].message == "example.com?api_key=****&sort=price"



def test_extra_do_redact_specific_key(caplog, logger_setup):
    logger = logger_setup([re.compile(r'\d{3}')])
    logger.warning("foo", extra={'phonenumber': 'foobar'})
    assert caplog.records[0].phonenumber == "****"
