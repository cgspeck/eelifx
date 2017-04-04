import yaml
from io import StringIO
from unittest.mock import Mock

from eelifx.config import dump_config, DEFAULT_CONFIG, load_config


def test_config_dump():
    assert yaml.load(dump_config()) == DEFAULT_CONFIG


def test_load_config():
    test_file_handle = StringIO('foo: bar')
    test_file_handle.close = Mock()
    assert load_config(test_file_handle) == {'foo': 'bar'}
    assert test_file_handle.close.called_once()


def test_load_config_invalid_yaml():
    test_file_handle = StringIO('foo: \'bar')
    test_file_handle.close = Mock()

    assert load_config(test_file_handle) is None
    assert test_file_handle.close.called_once()
