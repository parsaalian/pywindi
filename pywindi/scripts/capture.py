from pywindi.winclient import Winclient
import threading
import click
from time import sleep

ccd_time, ccd_temp, ccd_bin = 0.0, 0.0, (0.0, 0.0)
image_path = '/home/dimm/Desktop/images/'
address = ['localhost:7624']
clients = []

def add_address(host, port):
    address.append(host + ':' + str(port))


def add_clients():
    for a in address:
        host, port = a.split(':')
        client = Winclient(host, int(port))
        clients.append(client)


def take_image_with_one_client(client, time, temprature, binning):
    ccd = client.get_device('SBIG CCD')
    ccd.configure(image_directory=image_path)
    ccd.set_binning(binning[0], binning[1])
    ccd.set_temperature(temprature)
    ccd.take_image(time)


@click.command()
@click.option('--time', type=float, help='exposure time of image')
@click.option('--temprature', type=float, help='temprature of CCD for image')
@click.option('--binning', type=(float, float), help='binning of CCD for image')
@click.option('--interval', type=float, help='interval between images')
@click.option('--count', type=int, help='number of images to take')
def cli(time, temprature, binning, interval, count):
    ccd_time, ccd_temp, ccd_bin = time, temprature, binning
    add_clients()
    for i in range(count):
        threads = []
        for client in clients:
            t = threading.Thread(target=take_image_with_one_client, args=(client, ccd_time, ccd_temp, ccd_bin))
            threads.append(t)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        if not i == count - 1:
            print('Waiting', interval, 'seconds.')
            sleep(interval)
