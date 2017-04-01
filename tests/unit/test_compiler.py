from unittest.mock import sentinel, Mock, patch, call

from eelifx.util import compile_items


def test_compiler():
    '''
    Runs through a list of dicts, compiles string into code object and returns updated list
    '''
    uncomplied = [
        {
            'foo': 'True',
            'something_else': 'lol'
        },
        {
            'foo': 'False',
            'also_something_else': 'rofl'
        }
    ]

    mock_compile = Mock()
    mock_compile.side_effect = [sentinel.compiled_result_1, sentinel.compiled_result_2]

    expected = [
        {
            'foo': 'True',
            'foo_compiled': sentinel.compiled_result_1,
            'something_else': 'lol'
        },
        {
            'foo': 'False',
            'foo_compiled': sentinel.compiled_result_2,
            'also_something_else': 'rofl'
        }
    ]

    with patch('builtins.compile', mock_compile):
        assert compile_items(uncomplied, 'foo') == expected


def test_compiler_modes():
    '''
    Allows caller to specify whether compiling to exec or eval block
    '''
    uncomplied_1 = [
        {
            'foo': 'True',
        }
    ]
    uncomplied_2 = [
        {
            'foo': 'False',
        }
    ]

    mock_compile = Mock()
    mock_compile.side_effect = [sentinel.compiled_result_1, sentinel.compiled_result_2]

    expected_1 = [
        {
            'foo': 'True',
            'foo_compiled': sentinel.compiled_result_1,
        }
    ]
    expected_2 = [
        {
            'foo': 'False',
            'foo_compiled': sentinel.compiled_result_2,
        }
    ]

    with patch('builtins.compile', mock_compile):
        assert compile_items(uncomplied_1, 'foo') == expected_1
        assert compile_items(uncomplied_2, 'foo', mode='eval') == expected_2

    assert mock_compile.call_args_list == [
        call('True', '<string>', 'exec'),
        call('False', '<string>', 'eval')
    ]
