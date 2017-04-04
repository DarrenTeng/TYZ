import atexit
from pyVim.connect import SmartConnect, Disconnect

from config import VCConfig

def connect():
    try:
        config = VCConfig()
        si = SmartConnect(host=config.host,
                               user=config.user,
                               pwd=config.password,
                               port=config.port,
                               sslContext=config.sslContext)
        atexit.register(Disconnect, si)

    except IOError:
        return

    if not si:
        raise SystemError('Unable to connect to host with supplied info')

    return si

if __name__=='__main__':
    connect()
