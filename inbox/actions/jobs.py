""" Simple job dispatch implementation using rq.

This mechanism does not offer good durability in the case of catastrophic
failures---something to address on the next iteration.

"""
import rq

from redis import StrictRedis

from inbox.config import config
from inbox.util.concurrency import GeventWorker


def get_queue():
    # The queue label is set via config to allow multiple distinct Inbox
    # instances to hit the same Redis server without interfering with each
    # other.
    host = config.get_required('REDIS_HOST')
    port = config.get_required('REDIS_PORT')
    label = config.get_required('ACTION_QUEUE_LABEL')

    return rq.Queue(label, connection=StrictRedis(host=host, port=port, db=0))


# Later we're going to want to consider a pooling mechanism. We may want to
# split actions queues by remote host, for example, and have workers for a
# given host share a connection pool.
def rqworker(burst=False):
    """ Runs forever unless burst=True.

    More details on how workers work at: http://python-rq.org/docs/workers/

    """
    with rq.Connection():
        q = get_queue()

        w = GeventWorker([q])
        w.work(burst=burst)
