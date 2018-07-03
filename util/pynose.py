from unittest import SkipTest, TestCase
import functools
import types


def _id(obj):
    return obj


def skip(reason):
    """Unconditionally skip a test."""
    def decorator(test_item):
        if not isinstance(test_item, (type, types.ClassType)):
            @functools.wraps(test_item)
            def skip_wrapper(*args, **kwargs):
                raise SkipTest(reason)
            test_item = skip_wrapper
        elif issubclass(test_item, TestCase):
            @classmethod
            @functools.wraps(test_item.setUpClass)
            def skip_wrapper(*args, **kwargs):
                raise SkipTest(reason)
            test_item.setUpClass = skip_wrapper
        test_item.__unittest_skip__ = True
        test_item.__unittest_skip_why__ = reason
        return test_item
    return decorator


def skipIf(condition, reason):
    """Skip a test if the condition is true."""
    if not condition:
        return skip(reason)
    return _id
