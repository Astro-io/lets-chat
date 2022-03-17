from __future__ import print_function

import logging

import grpc
import chat_pb2
import chat_pb2_grpc
from time import sleep
import atexit

import signal
import sys
import time
import threading


token = None

channel = grpc.insecure_channel("localhost:6262")
client = chat_pb2_grpc.ChatStub(channel)


def login():
    global token
    response = client.Login(
        chat_pb2.LoginRequest(password="super-secret", name="test123")
    )
    token = response.token


def generate_messages():
    while True:
        msg = input()
        yield chat_pb2.StreamRequest(message=msg)


def chat():
    responses = client.Stream(generate_messages(), metadata=(("x-chat-token", token),))
    for response in responses:
        print(response.client_message.message)


def signal_handler(signal, frame):
    print("You pressed Ctrl+C!")
    sys.exit(0)


def exit_handler():
    client.Logout(chat_pb2.LogoutRequest(token=token))
    channel.close()


if __name__ == "__main__":
    logging.basicConfig()
    atexit.register(exit_handler)
    signal.signal(signal.SIGINT, signal_handler)
    login()
    chat()

    forever = threading.Event()
    forever.wait()
    print("Press Ctrl+C")
