from email.mime.text import MIMEText
import json
import pika
import smtplib
from fastapi import Depends, FastAPI, HTTPException

def send_email(studentEmail, body):
    try:
        sender_email = "cpsc449-backend@no-reply.com"

        message = MIMEText(body, "plain")
        message["From"] = sender_email
        message["To"] = studentEmail
        message["Subject"] = "Enrollment notification"

        with smtplib.SMTP("localhost", 8025) as server:
            server.sendmail(sender_email, studentEmail, message.as_string())

        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

def publish_email_notification(student_id: int, class_id: int, student_email: str):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='email', exchange_type='fanout')

        body = f"Student with id: {student_id} has been enrolled in Class {class_id}"
        jsonMessage = {"email" : student_email, "message" : body}
        message = json.dumps(jsonMessage)
        channel.basic_publish(exchange='email', routing_key='', body=message)
        connection.close()
    except Exception as e:
        print(f"Error publishing email notification: {e}")

def email_notification_consumer():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='email', exchange_type='fanout')
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='email', queue=queue_name)

        print(' [*] Waiting for email notifications')

        def callback(ch, method, properties, body):
            try:
                body_dict = json.loads(body.decode('utf-8'))
                studentEmail = body_dict.get("email")
                message = body_dict.get("message")
                send_email(studentEmail, message)
            except Exception as e:
                print(f"Error processing email message: {e}")
            finally:
                ch.basic_ack(delivery_tag=method.delivery_tag)
        channel.basic_consume(queue=queue_name, on_message_callback=callback)
        channel.start_consuming()

    except Exception as e:
        print(f"Error in email notification consumer: {e}")

if __name__ == '__main__':
    email_notification_consumer()
