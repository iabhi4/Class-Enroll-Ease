import json
import httpx
import pika
from urllib.parse import unquote
from fastapi import Depends, FastAPI, HTTPException

def send_webhook(proxyURL, body):
    try:
        url = unquote(proxyURL)
        r = httpx.post(url, data={'message': body})
        if r.status_code == 200:
            print('Webhook message sent')

    except Exception as e:
        print(f"Error sending webhook: {e}")

def publish_webhook_notification(student_id: int, class_id: int, proxyURL: str):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='webhook', exchange_type='fanout')

        body = f"Student with id: {student_id} has been enrolled in Class {class_id}"
        jsonMessage = {"proxyURL" : proxyURL, "message" : body}
        message = json.dumps(jsonMessage)
        channel.basic_publish(exchange='webhook', routing_key='', body=message)
        connection.close()
    except Exception as e:
        print(f"Error publishing webhook notification: {e}")

def webhook_notification_consumer():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='webhook', exchange_type='fanout')
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='webhook', queue=queue_name)

        print(' [*] Waiting for webhook notifications')

        def callback(ch, method, properties, body):
            try:
                body_dict = json.loads(body.decode('utf-8'))
                proxyURL = body_dict.get("proxyURL")
                message = body_dict.get("message")
                send_webhook(proxyURL, message)
            except Exception as e:
                print(f"Error processing webhook message: {e}")
            finally:
                ch.basic_ack(delivery_tag=method.delivery_tag)
        channel.basic_consume(queue=queue_name, on_message_callback=callback)
        channel.start_consuming()

    except Exception as e:
        print(f"Error in webhook notification consumer: {e}")

if __name__ == '__main__':
    webhook_notification_consumer()
