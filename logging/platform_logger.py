import logging
import json
from kafka import KafkaProducer
LOGGER_TOPIC = 'logging'


class KafkaHandler(logging.Handler):
    def __init__(self, sys_name, host_port, topic):
        logging.Handler.__init__(self)
        self.producer = KafkaProducer(bootstrap_servers=[
            host_port], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        self.topic = topic
        self.sys_name = sys_name

    def emit(self, record):
        if 'kafka.' in record.name:
            return
        try:
            self.formatter = logging.Formatter(
                '%(asctime)s ::: %(name)s ::: %(levelname)s ::: %(message)s')
            msg = self.format(record).strip()
            self.producer.send(self.topic, {
                'timestamp': record.asctime,
                'level': record.levelname,
                'sys_name': self.sys_name,
                'message': record.message})
            self.flush(timeout=1.0)
        except:
            logging.Handler.handleError(self, record)

    def flush(self, timeout=None):
        self.producer.flush(timeout=timeout)

    def close(self):
        try:
            if self.producer:
                self.producer.close()
            logging.Handler.close(self)
        finally:
            self.release()


def get_logger(sys_name, host_port, level=logging.DEBUG):
    logger = logging.getLogger(sys_name)
    logger.setLevel(level)
    kh = KafkaHandler(sys_name, host_port, LOGGER_TOPIC)
    logger.addHandler(kh)
    return logger
