class config(object):
    """description of class"""
    pass

import ssl


class Config:
    pass


class VCConfig(Config):
    host = '10.224.104.49'
    user = 'nqwang@vsphere.local'
    password = 'nqwang'
    port = 443
    sslContext = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
    sslContext.verify_mode = ssl.CERT_NONE


class TemplateConfig(Config):
    username = 'Administrator'
    password = 'rockwell123@RA'
