import zmq
import logging
from decouple import config

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT, level="INFO")
logger = logging.getLogger(__name__)

HOST = config("MT5_REALTIME_HOST", default="127.0.0.1")
PORT = config("MT5_REALTIME_PORT", default="5557")

MT5_REALTIME_PRICE_CHANNEL = "mt5_real_time_price"


# Creates a socket instance
context = zmq.Context()
subscriber = context.socket(zmq.SUB)

# Connects to a bound socket
subscriber.connect("tcp://{}:{}".format(HOST, PORT))

# Subscribes to all topics
subscriber.subscribe("PETR4")

# Receives a string format message
poller = zmq.Poller()

poller.register(subscriber, zmq.POLLIN)

logger.info("MT5 Real Time Client Started")
while True:
    try:
        socks = dict(poller.poll())
    except KeyboardInterrupt:
        break

    if subscriber in socks:
        message = subscriber.recv()
        logger.info(f"Command received: {message}")