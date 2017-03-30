import logging
from pprint import pformat


def compile_items(_list, item_key):
    for item in _list:
        if item_key not in item:
            logging.warning(
                "Could not find %s in object %s.",
                item_key,
                item
            )
            next
        try:
            item['%s_compiled' % item_key] = compile(item[item_key], '<string>', 'exec')
        except Exception as e:
            logging.exception("Unable to compile the following code to a python code object: %s" % pformat(item[item_key]))
            raise
