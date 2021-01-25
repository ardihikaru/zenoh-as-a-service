from zenoh_service.zenoh_native_put import ZenohNativePut
import sys
import logging

###

L = logging.getLogger(__name__)


###

path = "/demo/example/test3"
value = 123
pub = ZenohNativePut(
	_path=path, _session_type="PUT"
)
pub.init_connection()

# put data
pub.put(value)

# closing Zenoh subscription & session
pub.close_connection()
