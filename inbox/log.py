"""
Logging configuration.

Mostly based off http://www.structlog.org/en/0.4.1/standard-library.html.

"""
import sys
import socket
import traceback

from collections import OrderedDict

import requests
import structlog

from inbox.config import config

import logging
logging.basicConfig(level=logging.INFO,
                    format="%(message)s")

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
get_logger = structlog.get_logger


def email_exception(logger, etype, evalue, tb):
    """ Send stringified exception to configured email address. """
    exc_email_addr = config.get('EXCEPTION_EMAIL_ADDRESS')
    if exc_email_addr is None:
        logger.error("No EXCEPTION_EMAIL_ADDRESS configured!")
    mailgun_api_endpoint = config.get('MAILGUN_API_ENDPOINT')
    if mailgun_api_endpoint is None:
        logger.error("No MAILGUN_API_ENDPOINT configured!")
    mailgun_api_key = config.get('MAILGUN_API_KEY')
    if mailgun_api_key is None:
        logger.error("No MAILGUN_API_KEY configured!")

    r = requests.post(
        mailgun_api_endpoint,
        auth=("api", mailgun_api_key),
        data={"from": "Inbox App Server <{}>".format(exc_email_addr),
              "to": [exc_email_addr],
              "subject": "Uncaught error! {} {}".format(etype, evalue),
              "text": u"""
    Something went wrong on {}. Please investigate. :)

    {}

    """.format(socket.getfqdn(),
               '\t'.join(traceback.format_exception(etype, evalue, tb)))})
    if r.status_code != requests.codes.ok:
        logger.error("Couldn't send exception email: {}".format(r.json()))


def log_uncaught_errors(logger=None):
    """ Helper to log uncaught exceptions.

    Parameters
    ----------
    logger: structlog.BoundLogger, optional
        The logging object to write to.
    """
    logger = logger or get_logger()
    logger.exception('Uncaught error')
    if config.get('EMAIL_EXCEPTIONS'):
        email_exception(logger, *sys.exc_info())

    def __str__(self):
        return str(self.func)

    def __repr__(self):
        return repr(self.func)

    def __getattr__(self, item):
        return getattr(self.func, item)
