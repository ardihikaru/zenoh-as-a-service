from zenoh_service.core.zenoh_net import ZenohNet
from zenoh_service.zenoh_net_subscriber import ZenohNetSubscriber
import sys
import time
from datetime import datetime
import logging

###

L = logging.getLogger(__name__)


###


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
