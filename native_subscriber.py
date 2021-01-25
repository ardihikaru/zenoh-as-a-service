from zenoh_service.zenoh_native_subscriber import ZenohNativeSubscriber
import sys
import logging

###

L = logging.getLogger(__name__)


###

selector = "/demo/**"
sub = ZenohNativeSubscriber(
	_selector=selector, _session_type="SUBSCRIBER"
)
sub.init_connection()

sub.register()
subscriber = sub.get_subscriber()
L.warning("[ZENOH] Press q to stop...")
c = '\0'
while c != 'q':
	c = sys.stdin.read(1)

# closing Zenoh subscription & session
sub.close_connection(subscriber)
