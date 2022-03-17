# lets-chat

In this exercise a team will build a chat server and a two clients. The end
result should behave the same way as the example docker image provided.

It is a requirement that the provided proto (grpc) is used.

The main focus should be on finishing (over correctness and pretty code) and working together.

#### Suggested steps

 - Create a private git repo and clone it (push often to make sure your coworkers can access the code)
 - Take a grpc quick start and understand the basics, compile the python classes from the proto (https://grpc.io/docs/languages/python/quickstart/)
 - Setup a grpc boilerplate server and client, can we connect the client to the server? 
 - Read the proto and the comments, touch briefly on grpc metadata.
 - Discuss the implementation of the server/client, what data needs to be in memory while running, how will the server broadcast, are multiple threads needed?
 - Decide on the languages used for clients and servers and get started on compiling the protos for that language. (https://grpc.io/docs/languages/)
 - Who is doing what? Some should work on the server, others on the clients. Help each other.
 - (optional) Deploy the server on a VM or even better create a docker image(env PYTHONUNBUFFERED=1 might be helpful) and host this as a kubernetes service (with type loadbalancer)
 - (optional) Test that you can connect to the deployment from your local machines

Remember you have the docker `eu.gcr.io/brunsgaard-public/chat-exercise` to
help test functionality. Login/Logout/Shutdown events should be broadcasted and printed the
same way as in the example docker image.


First we make it work, then we make it pretty. This exersice focuses on making it work.


### Usage of example implementation
![chat](chat.png)
The hex part strings you see from the server is the tokens return in
LoginResponse, when calling the Stream method in the service the token should
be supplied in a HTTP header (grpc metadata) called `x-chat-token`.
```
docker network create chat-net
docker run --rm --network=chat-net --name=chat-server -p 6262:6262 eu.gcr.io/brunsgaard-public/chat-exercise -s -p "super-secret"
# In another terminal setup a client
docker run -i --rm --network=chat-net eu.gcr.io/brunsgaard-public/chat-exercise -h "chat-server:6262" -p "super-secret" -n "brunsgaard"

```

### Build protos for Python
```
bash-3.2$ python -m pip install virtualenv
bash-3.2$ source venv/bin/activate
(venv) bash-3.2$ python -m pip install --upgrade pip
(venv) bash-3.2$ python -m pip install grpcio
(venv) bash-3.2$ python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. chat.proto
(venv) bash-3.2$ ls
README.md		chat.png		chat.proto		chat_pb2.py		chat_pb2_grpc.py	venv
(venv) bash-3.2$
```
