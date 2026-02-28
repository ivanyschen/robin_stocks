"""Holds the session header and other global variables."""
import sys
import os

from requests import Session

import threading
from requests import Session

# Thread-local storage for keeping sessions isolated per concurrent user
_thread_local = threading.local()

def get_session():
    """Returns a thread-local requests.Session object configured for robin_stocks."""
    if not hasattr(_thread_local, "session"):
        _thread_local.session = Session()
        _thread_local.session.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip,deflate,br",
            "Accept-Language": "en-US,en;q=1",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "X-Robinhood-API-Version": "1.431.4",
            "Connection": "keep-alive",
            "User-Agent": "*"
        }
    return _thread_local.session

def get_logged_in():
    """Returns the thread-local login state."""
    if not hasattr(_thread_local, "logged_in"):
        _thread_local.logged_in = False
    return _thread_local.logged_in

def set_logged_in(state):
    """Sets the thread-local login state."""
    _thread_local.logged_in = state

# For backwards compatibility with single-thread scripts that import SESSION
# We use __getattr__ for module level to intercept old 'SESSION' imports if using Python 3.7+
def __getattr__(name):
    if name == 'SESSION':
        return get_session()
    if name == 'LOGGED_IN':
        return get_logged_in()
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

#All print() statement direct their output to this stream
#by default, we use stdout which is the existing behavior
#but a client can change to any normal Python stream that
#print() accepts.  Common options are
#sys.stderr for standard error
#open(os.devnull,"w") for dev null
#io.StringIO() to go to a string for the client to inspect
OUTPUT=sys.stdout
