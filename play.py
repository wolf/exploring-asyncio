# play.py

from types import coroutine
from collections import deque
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

@coroutine
def read_wait(sock):
    yield 'read_wait', sock


@coroutine
def write_wait(sock):
    yield 'write_wait', sock

class Loop:
    def __init__(self):
        self.ready = deque()
        self.selector = DefaultSelector()

    async def sock_recv(self, sock, maxbytes):
        await read_wait(sock)
        return sock.recv(maxbytes)

    async def sock_accept(self, sock):
        await read_wait(sock)
        return sock.accept()

    async def sock_sendall(self, sock, data):
        while data:
            try:
                nsent = sock.send(data)
                data = data[nsent:]
            except BlockingIOError:
                await write_wait(sock)

    def create_task(self, coro):
        self.ready.append(coro)

    def run_forever(self):
        while True:
            while not self.ready:
                events = self.selector.select()
                for key, _ in events:
                    self.ready.append(key.data)
                    self.selector.unregister(key.fileobj)
            while self.ready:
                self.current_task = self.ready.popleft()
                try:
                    op, *args = self.current_task.send(None) # Run to the yield
                    getattr(self, op)(*args) # Sneaky method call
                except StopIteration:
                    pass

    def read_wait(self, sock):
        self.selector.register(sock, EVENT_READ, self.current_task)

    def write_wait(self, sock):
        self.selector.register(sock, EVENT_WRITE, self.current_task)
