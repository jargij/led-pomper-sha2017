# led-pomper-sha2017

During the SHA2017 there was a led screen in the main bar available to 'hack'.
Because everyone was pushing pixels to it, we came up with the idea to spread
the image we wanted to display over a scalable number of workers.

# Dependencies
- Python 3.5
  - Pillow
  - Pika
- RabbitMQ

# Workers
Workers can be provisioned by changing some vars in sender.py.
They read the available payload from the queue in RabbitMQ and push it to the defined server on the desired port.

# 'Manager'
With the img_to_queue.py script you are able to slice png images into small pieces that each of the workers is going to take care of.
```
img_to_queue.py -i <inputfile> -w <amountofworkers>
```
There are two parameters that this script takes:
- -i is the file that you want to display
- -w is the amount of workers that are available. This root square of this number needs to be a round number.

# Disclaimer
This project was made as fast as possible, some of the things could be done in a better way. But yeah, still hacking anyway...
