# This file is part of the GNU Health GTK Client.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from jsonrpc import Fault

TrytonServerError = Fault


class TrytonServerUnavailable(Exception):
    pass


class TrytonError(Exception):

    def __init__(self, faultCode):
        self.faultCode = faultCode
