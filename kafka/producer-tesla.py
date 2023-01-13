# Code inspired from Confluent Cloud official examples library
# https://github.com/confluentinc/examples/blob/7.1.1-post/clients/cloud/python/producer.py

from confluent_kafka import Producer
import json
import ccloud_lib # Library not installed with pip but imported from ccloud_lib.py
import numpy as np
import time

# Initialize configurations from "python.config" file
CONF = ccloud_lib.read_ccloud_config("python.config")
TOPIC = "nasdaq_prices"

# Create Producer instance
producer_conf = ccloud_lib.pop_schema_registry_params_from_config(CONF)
producer_topic = ccloud_lib.create_topic(CONF, TOPIC)
producer = Producer(producer_conf)

import requests

url = "https://realstonks.p.rapidapi.com/TSLA"

headers = {
	"X-RapidAPI-Key": "dc9665504emshd4b02932d40379bp1b60dcjsn1177cf22dd2f",
	"X-RapidAPI-Host": "realstonks.p.rapidapi.com"
}

#print(data["price"])

def acked(err, msg):
    global delivered_records
    delivered_records = 0

    if err is not None:
        print("Failed to deliver message: {}".format(err))
    else:
        delivered_records +=1
        print("Produced record to topic {} partition [{}] @ offset {}".format(msg.topic(), msg.partition(), msg.offset()))

try:
    # Starts an infinite while loop that produces random current temperatures
    while True:

        response = requests.request("GET", url, headers=headers)

        data = json.loads(response.text)

        record_key = "tesla_price"
        
        record_value = json.dumps(
            {
                "time_of_price": response.headers.get("Date"),
                "current_price": data["price"] 
            }
        )
        
        print("Producing record: {}\t{}".format(record_key, record_value))

        # This will actually send data to your topic
        producer.produce(
            TOPIC,
            key=record_key,
            value=record_value,
            #on_delivery=acked
        )
        producer.poll(0)
        time.sleep(1)
        

 # Interrupt infinite loop when hitting CTRL+C
except KeyboardInterrupt:
    pass
finally:
    producer.flush() # Finish producing the latest event before stopping the whole script
