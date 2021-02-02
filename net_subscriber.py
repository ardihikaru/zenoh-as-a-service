from zenoh_service.core.zenoh_net import ZenohNet
from zenoh_service.zenoh_net_subscriber import ZenohNetSubscriber
import sys
import time
from datetime import datetime
import logging

###

L = logging.getLogger(__name__)


###

# # Scenario 1: Simple Pub/Sub with a single PC
# selector = "/demo/**"

# Scenario 2: Pub/Sub with two hosts
"""
	Simulated scenario:
	- `Host #01` will has IP `192.168.1.110`
	- `Host #01` run `subscriber`
	- `Host #02` run `publisher`
	- Asumming that both hosts are in the multicast network environment
"""
selector = "/demo/**"
listener = "tcp/192.168.1.110:7447"

sub = ZenohNetSubscriber(
	_selector=selector, _session_type="SUBSCRIBER", _listener=listener
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
