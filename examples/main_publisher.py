import sys
import time
from datetime import datetime
import numpy as np
import cv2
import simplejson as json
from enum import Enum
import zenoh
from zenoh.net import config, SubInfo, Reliability, SubMode, Sample, resource_name
from zenoh.net.queryable import STORAGE
import logging

###

L = logging.getLogger(__name__)


###

class ZenohNet(object):
	"""
	A higher level API providing the same abstractions as the zenoh-net API in a simpler and more data-centric oriented
	manner as well as providing all the building blocks to create a distributed storage. The zenoh layer is aware of
	the data content and can apply content-based filtering and transcoding.
	(source: http://zenoh.io/docs/getting-started/key-concepts/)

	Available functionalities:
		[1] write : push live data to the matching subscribers.
		[2] subscribe : subscriber to live data.
		[3] query : query data from the matching queryables.
		[4] queryable : an entity able to reply to queries.

	Implemented scenarios:
	1. Zenoh SUBSCRIBER with STORAGE (Queryable)
		Sample input: listener=None, mode='peer', peer=None, selector='/demo/example/**'
	2. Zenoh PUBLISHER
		Sample input: listener=None, mode='peer', path='/demo2/example/test', peer=None, value='Hello World'
	3. Zenoh GET
		Sample input: listener=None, mode='peer', peer=None, selector='/demo/example/**'
	"""

	class ZenohMode(Enum):
		PEER = "peer"
		CLIENT = "client"

	class SessionType(Enum):
		SUBSCRIBER = "SUBSCRIBER"
		PUBLISHER = "PUBLISHER"

	# set default encoder
	ENCODER = [
		('id', 'U10'),
		('timestamp', 'f'),
		('data', [('flatten', 'i')], (1, 6220800)),
		('store_enabled', '?'),
	]

	def __init__(self, _listener=None, _mode="peer", _peer=None, _selector=None, _path=None, _session_type=None,
	             type_numpy=False, tagged_data=False):
		self.listener = _listener  # Locators to listen on.
		self.mode = _mode  # The zenoh session mode.
		self.peer = _peer  # Peer locators used to initiate the zenoh session.
		self.selector = _selector  # The selection of resources to subscribe.
		self.path = _path  # The name of the resource to put.
		self.session_type = self._get_session_type(_session_type)  # Type of Zenoh connection
		self.type_numpy = type_numpy  # Expected type of the extracted data

		if type_numpy:  # to be assigned only when the type is a numpy array
			self.tagged_data = tagged_data  # When tagged, data will be an encoded into list
			"""
			Sample data of `tagged_data`
			[
				<id: String>,
				<timestamp: Float>,
				<data: Numpy array>,
				<other1: some_data_type>
			]
			"""

		# setup configuration
		self.conf = {"mode": self.mode}
		if self.peer is not None:
			self.conf["peer"] = self.peer
		if self.listener is not None:
			self.conf["listener"] = self.listener

		self.z_session = None
		self.z_sub_info = None
		self.z_queryable = None
		self.z_rid = None

		self.pub = None
		self.sub = None

	def _get_session_type(self, _type):
		if _type.upper() == self.SessionType.SUBSCRIBER.value:
			return self.SessionType.SUBSCRIBER.value
		elif _type.upper() == self.SessionType.PUBLISHER.value:
			return self.SessionType.PUBLISHER.value
		else:
			return None

	def init_connection(self):
		# initiate logging
		zenoh.init_logger()

		L.warning("[ZENOH] Openning session...")
		self.z_session = zenoh.net.open(self.conf)

		self.z_sub_info = SubInfo(Reliability.Reliable, SubMode.Push)

	def close_connection(self, _subscriber=None):
		self.z_session.close()
		L.warning("[ZENOH] `{}` session has been closed".format(self.session_type))

	def register_subscriber(self, listener, queryable=False):
		L.warning("[ZENOH] Registering new consumer")
		self.sub = self.z_session.declare_subscriber(self.selector, self.z_sub_info, listener)

		if queryable:
			L.warning("[ZENOH] Declaring Queryable on '{}'...".format(selector))
			self.z_queryable = self.z_session.declare_queryable(
				self.selector, STORAGE, query_handler)

	def register_publisher(self):
		L.warning("[ZENOH] Registering new producer")
		self.z_rid = self.z_session.declare_resource(self.path)
		self.pub = self.z_session.declare_publisher(self.z_rid)

	def publish_data(self, encoded_val):
		L.warning("[ZENOH] Publish data")
		self.z_session.write(self.z_rid, encoded_val)


class ZenohNetPublisher(ZenohNet):

	class InputDataType(Enum):
		NATIVE_TYPE = 1
		SIMPLE_NUMPY = 2
		COMPLEX_NUMPY = 3

	def __init__(self, _listener=None, _mode="peer", _peer=None, _path=None, _session_type=None):
		super().__init__(_listener=_listener, _mode=_mode, _peer=_peer, _path=_path, _session_type=_session_type)

	def register(self):
		super().register_publisher()

	def get_publisher(self):
		return self.pub

	def _get_encoder(self, _encoder):
		return self.ENCODER if _encoder is None else _encoder

	def _encode_data(self, _val, _itype, _encoder):
		if _itype == self.InputDataType.NATIVE_TYPE.value:
			encoded_data = bytes(json.dumps(_val), encoding='utf8')
		elif _itype == self.InputDataType.SIMPLE_NUMPY.value:
			encoded_data = _val.tobytes()
		elif _itype == self.InputDataType.COMPLEX_NUMPY.value:
			encoder = self._get_encoder(_encoder)
			tagged_data = np.array(_val, dtype=encoder)
			encoded_data = tagged_data.tobytes()
		else:
			# simply convert the data into bytes
			encoded_data = bytes(json.dumps(_val), encoding='utf8')

		return encoded_data

	# def publish(self, _val, _itype, _encoder=None, _taggable_info=None):
	def publish(self, _val, _itype, _encoder=None):
		"""
		_val: The value of the resource to put.
		"""

		# pre-process data before being sent into Zenoh system
		encoded_data = self._encode_data(_val, _itype, _encoder)

		t0_publish = time.time()
		super().publish_data(encoded_data)
		t1_publish = (time.time() - t0_publish) * 1000
		L.warning(('\n[%s] Latency insert data into Zenoh (%.3f ms) \n' % (datetime.now().strftime("%H:%M:%S"), t1_publish)))

	def close_connection(self, _producer=None):
		if _producer is not None:
			_producer.undeclare()
		super().close_connection()


# """
# Usage example
# ---------------

# Define input data
# [1] Data Type: simple Integer / Float / Bool
# encoder_format = None
# itype = 1
# val = 123
###############################################################

# [2] Data Type: Numpy Array (image)
# encoder_format = None
# itype = 2
# root_path = "/home/s010132/devel/eagleeye/data/out1.png"
# val = cv2.imread(root_path)
###############################################################

# [3] Data Type: Numpy Array with structured array format (image + other information)
itype = 3
encoder_format = [
	('id', 'U10'),
	('timestamp', 'f'),
	('data', [('flatten', 'i')], (1, 6220800)),
	('store_enabled', '?'),
]
root_path = "/home/s010132/devel/eagleeye/data/out1.png"
img = cv2.imread(root_path)
img_1d = img.reshape(1, -1)
val = [('Drone 1', time.time(), img_1d, False)]
###############################################################

# configure zenoh service
ip_addr = "localhost"
peer = "tcp/{}:7447".format(ip_addr)
path = "/demo/example/zenoh-python-pub"
z_svc = ZenohNetPublisher(
	_path=path, _session_type="PUBLISHER", _peer=peer
)
z_svc.init_connection()

# register and collect publisher object
z_svc.register()
publisher = z_svc.get_publisher()

# publish data
z_svc.publish(
	_val=val,
	_itype=itype,
	_encoder=encoder_format,
)

# closing Zenoh publisher & session
z_svc.close_connection(publisher)
# """
