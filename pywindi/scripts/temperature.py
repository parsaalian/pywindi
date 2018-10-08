from pywindi.winclient import Winclient
import click

address = ''

def get_temp(address):
    host, port = address.split(':')
    client = Winclient(host, int(port))
    ccd = client.get_device('SBIG CCD')
    try:
        ccd = client.get_device('SBIG CCD')
    except Exception as e:
        print(e)
        print('Couldn\'t connect to', address, 'server.')
        return
    temp = ccd.get_temperature()
    client.disconnectServer()
    return temp

@click.command()
@click.option('--addr', type=str, help='address of ccd to get temperature from')
def temp_cli(addr):
    global address
    address = addr
    return get_temp(address)
