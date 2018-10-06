from pywindi.winclient import Winclient
import click

def get_temperature(address):
    host, port = address.split(':')
    client = Winclient(host, port)
    ccd = client.get_device('SBIG CCD')
