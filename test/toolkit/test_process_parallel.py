import functools
import logging

from stograde.toolkit.process_parallel import process_parallel


def a_function(name: str):
    logging.info('a_function: {}'.format(name))


def test_process_parallel_single_thread(caplog):
    operation = functools.partial(a_function)
    with caplog.at_level(logging.DEBUG):
        process_parallel(['student1'],
                         no_progress_bar=True,
                         workers=1,
                         operation=operation)

    log_messages = {(log.msg, log.levelname) for log in caplog.records}
    assert log_messages == {('Processing student1', 'DEBUG'),
                            ('a_function: student1', 'INFO')}
