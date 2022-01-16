# Notes for development

## Server sent events
TODO: Make the endpoint `"/listen"` the subscriber to all the data-services that update the database.
```
# in each of the _resources
announcer.announce(data)

# in /listen
def stream():
    messages = announcer.listen()  # returns a queue.Queue
    while True:
        msg = messages.get()  # blocks until a new message arrives
        yield msg
```

Enable authentication with the sse access

## Organizing routes in `__init__.py`