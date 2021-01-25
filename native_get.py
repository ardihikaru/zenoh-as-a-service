"""
This script will only be able to collect information if the data is stored
logic in `native_subscriber.py` is not storing the data. it purely consume the information
"""
from zenoh_service.zenoh_native_get import ZenohNativeGet
import logging

###

L = logging.getLogger(__name__)


###

# configure input parameters
# selector = "/demo/example/**"
selector = "/demo/image/**"
type_image = True
tagged_image = True

z_svc = ZenohNativeGet(
	_selector=selector, _session_type="GET",
	type_image=type_image, tagged_image=tagged_image
)
z_svc.init_connection()

z_svc.get()

# closing Zenoh subscription & session
z_svc.close_connection()
# """
