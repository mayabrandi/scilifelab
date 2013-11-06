"""
log module
"""
import sys
import logging
import logbook

from scilifelab.utils import config as cf
from logbook.queues import RedisHandler

try:
    import bcbio.pipeline.config_utils as cl
except ImportError:
    import bcbio.pipeline.config_loader as cl

def minimal_logger(namespace, extra_fields=None, debug=False):
    """Make and return a minimal console logger.

    NOTE: this does apparently *not* work with logbook as I first thought, and
    log handlers will *not* take care of output. If something is to be
    logged to a file in a module, the logger has to be implemented for
    that particular purpose.

    The current function is copied from cement.core.backend.

    :param namespace: namspace of logger
    """
    config = cf.load_config()
    log = logbook.Logger(namespace, level=logbook.INFO)
    s_h = logbook.StreamHandler(sys.stdout, level = logbook.INFO, bubble=True)
    log.handlers.append(s_h)
    try:
        host = config.get('log', 'redis_host')
        port = config.getint('log', 'redis_port')
        key = config.get('log', 'redis_key')
        password = config.get('log', 'redis_password')
        if not extra_fields:
            extra_fields = {"program": "pm",
                            "command": namespace}
        r_h = RedisHandler(host=host, port=port, key=key, password=password,
                extra_fields=extra_fields, level=logbook.INFO, bubble=True)
        log.handlers.append(r_h)
    except:
        log.warn('Not loading RedisHandler')
        pass

    # FIX ME: really don't want to hard check sys.argv like this but
    # can't figure any better way get logging started (only for debug)
    # before the app logging is setup. Besides, this will fail for
    # tests since sys.argv will consist of the test call arguments.
    if '--debug' in sys.argv or debug:
        try:
            #If there was any problem loading the RedisHandler, at this point
            #the variable r_h will not exist
            r_h.level = logbook.DEBUG
        except UnboundLocalError:
            pass
        s_h.level = logbook.DEBUG
        log.level = logbook.DEBUG

    return log



def file_logger(namespace, config_file, log_file):
        CONFIG = cl.load_config(config_file)
        log_path = CONFIG['log_dir'] + '/' + log_file

        logger = logging.getLogger(namespace)
        logger.setLevel(logging.DEBUG)

        # file handler
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.INFO)

        # console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # formatter
        formatter = logging.Formatter("%(asctime)s (%(levelname)s) : %(message)s")
        fh.setFormatter(formatter)

        # add handlers to logger
        logger.addHandler(ch)
        logger.addHandler(fh)

        return logger
