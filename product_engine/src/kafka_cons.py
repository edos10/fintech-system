from common.kafka import ConsumerKafkaProcessing

def print_msg(msg: bytes):
    print(msg)

agreements_consumer = ConsumerKafkaProcessing(print_msg, "new-agreements")