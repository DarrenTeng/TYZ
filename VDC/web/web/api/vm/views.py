from web import app
from . import vm

@vm.route('/')
@vm.route('/home')
def home():
    return 'This is api for virtual machine.'
