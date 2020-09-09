import logging
from logging import config  # noqa


class ColorFormatter(logging.Formatter):

    BLUE = '\033[1;94m'
    GREEN = '\033[1;92m'
    YELLOW = '\033[1;93m'
    RED = '\033[1;91m'
    END_TAG = '\033[0m'

    COLOR_DICT = {
        logging.DEBUG: BLUE,
        logging.INFO: GREEN,
        logging.WARNING: YELLOW,
        logging.ERROR: RED
    }

    def format(self, record):
        message = logging.Formatter.format(self, record)

        color = self.COLOR_DICT.get(record.levelno)

        return "{color}{message}{end_tag}".format(color=color, message=message, end_tag=self.END_TAG)


default_config = {
    'version': 1,
    'formatters': {
        'default':
            {
                '()': 'pandora.logs.ColorFormatter',
                'format': "%(asctime)s - %(levelname)s:%(name)s: %(message)s"
            }
    },
    'handlers': {
        'default': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'root': {
        'level': logging.INFO,
        'handlers': ['default'],
    }
}


def configure(debug=False):
    if debug:
        default_config['root']['level'] = logging.DEBUG

    logging.config.dictConfig(default_config)