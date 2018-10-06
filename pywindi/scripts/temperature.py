from pywindi.winclient import Winclient
import click

address = ''

def get_temperature(address):
    host, port = address.split(':')
    client = Winclient(host, port)
    ccd = client.get_device('SBIG CCD')
    try:
        ccd = client.get_device('SBIG CCD')
    except Exception as e:
        print(e)
        print('Couldn\'t connect to', address, 'server.')
        return
    return ccd.get_temperature()

@click.command()
@click.option('--addr', type=str, help='address of ccd to get temperature from')
def get_temperature_cli(addr):
    global address
    address = addr
    return get_temperature(address)
