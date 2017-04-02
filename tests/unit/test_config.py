import yaml

from eelifx.config import dump_config, DEFAULT_CONFIG


def test_config_dump():
    assert yaml.load(dump_config()) == DEFAULT_CONFIG
