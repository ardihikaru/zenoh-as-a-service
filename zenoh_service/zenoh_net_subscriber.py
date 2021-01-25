from zenoh_service.core.zenoh_net import ZenohNet
import sys
import time
from datetime import datetime
import logging

###

L = logging.getLogger(__name__)


###


def listener(consumed_data):
	L.warning("Consumed Value: {}".format(consumed_data.payload))
	# store[sample.res_name] = (change.payload, change.data_info)


def query_handler(query):
	L.warning(">> [Query handler   ] Handling '{}?{}'"
          .format(query.res_name, query.predicate))
	replies = []
	for stored_name, (data, data_info) in store.items():
		if resource_name.intersect(query.res_name, stored_name):
			query.reply(Sample(stored_name, data, data_info))


class ZenohNetSubscriber(ZenohNet):
	def __init__(self, _listener=None, _mode="peer", _peer=None, _selector=None, _session_type=None):
		super().__init__(_listener=_listener, _mode=_mode, _peer=_peer, _selector=_selector, _session_type=_session_type)

	def register(self):
		super().register_subscriber(listener)

	def get_subscriber(self):
		return self.sub

	def close_connection(self, _subscriber=None):
		if _subscriber is not None:
			_subscriber.undeclare()
		if self.z_queryable is not None:
			self.z_queryable.undeclare()
		super().close_connection()


"""
# Usage example
# ---------------

selector = "/demo/**"
sub = ZenohNetSubscriber(
	_selector=selector, _session_type="SUBSCRIBER"
)
sub.init_connection()

sub.register()
subscriber = sub.get_subscriber()
L.warning("[ZENOH] Press q to stop...")
c = '\0'
while c != 'q':
	c = sys.stdin.read(1)

# # closing Zenoh subscription & session
sub.close_connection(subscriber)
"""
