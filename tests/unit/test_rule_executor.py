import pytest
from unittest.mock import Mock

from eelifx.processor import run_rules

standard_effect = 'lifx_commanders[lc_index].set_colour("green")'

testdata_single_rules = [
    ('A rule which returns False', 'False', standard_effect, False),
    ('A rule which returns True', 'True', standard_effect, True),
]

testdata_multiple_rules = [
    ('A rule which returns True', 'True', 'lifx_commanders[lc_index].set_colour("green")'),
    ('A rule which returns False', 'False', 'lifx_commanders[lc_index].set_power(False)'),
    ('Another rule which returns True', 'True', 'lifx_commanders[lc_index].set_luminance(0.8)'),
]

testdata_ship_state_rules = [
    ('Ship state satisfies rule', 'ship.alert_level == "RED ALERT"', standard_effect, True),
    ('Ship state does not satisfy rule', 'ship.alert_level == "normal"', standard_effect, False),
]


def mock_commander_factory():
    mock_commander = Mock()
    mock_commander.set_colour = Mock()
    mock_commander.set_luminance = Mock()
    mock_commander.set_power = Mock()
    mock_commander.set_effect = Mock()
    return mock_commander


@pytest.fixture
def mock_commanders():
    return [mock_commander_factory(), mock_commander_factory()]


@pytest.fixture
def mock_ship():
    ship = Mock()
    ship.alert_level = Mock(return_value='RED ALERT')
    return ship


@pytest.mark.parametrize('scenario,statement,effect,expected_to_be_triggered', testdata_single_rules)
def test_rule_executor(
    scenario,
    statement,
    effect,
    expected_to_be_triggered,
    mock_commanders,
    mock_ship
):
    lc_index = 0
    rules = []
    rules.append(dict(
        statement=statement,
        statement_compiled=compile(statement, '<string>', 'eval'),
        effect=effect,
        effect_compiled=compile(effect, '<string>', 'exec')
    ))

    run_rules(
        lc_index,
        mock_commanders,
        mock_ship,
        rules
    )

    if expected_to_be_triggered:
        assert mock_commanders[lc_index].set_colour.called
    else:
        assert not mock_commanders[lc_index].set_colour.called


@pytest.mark.parametrize('scenario,statement,effect,expected_to_be_triggered', testdata_single_rules)
def test_rule_executor_ship_state(
    scenario,
    statement,
    effect,
    expected_to_be_triggered,
    mock_commanders,
    mock_ship
):
    lc_index = 0
    rules = []
    rules.append(dict(
        statement=statement,
        statement_compiled=compile(statement, '<string>', 'eval'),
        effect=effect,
        effect_compiled=compile(effect, '<string>', 'exec')
    ))

    run_rules(
        lc_index,
        mock_commanders,
        mock_ship,
        rules
    )

    if expected_to_be_triggered:
        assert mock_commanders[lc_index].set_colour.called
    else:
        assert not mock_commanders[lc_index].set_colour.called


def test_multiple_rules(mock_commanders, mock_ship):
    lc_index = 0
    rules = []
    for rule in testdata_multiple_rules:
        rules.append(dict(
            statement=rule[1],
            statement_compiled=compile(rule[1], '<string>', 'eval'),
            effect=rule[2],
            effect_compiled=compile(rule[2], '<string>', 'exec')
        ))

    run_rules(
        lc_index,
        mock_commanders,
        mock_ship,
        rules
    )

    assert mock_commanders[lc_index].set_colour.called
    assert not mock_commanders[lc_index].set_power.called
    assert mock_commanders[lc_index].set_luminance.called
