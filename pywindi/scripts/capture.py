from pywindi.winclient import Winclient
import threading
import click
from time import sleep

file = open('ccd_base_config.txt', 'r')

ccd_num, ccd_time, ccd_temp, ccd_bin = 1, 0.0, 0.0, (1.0, 1.0)
#: path where image is saved.
image_path = file.readline()[:-1]
#: list of hosts.
addresses = file.readline()[1:-1].replace(' ', '').split(',')
clients = []
file_names = []

def add_address(host, port = 7624):
    addresses.append(host + ':' + str(port))


def delete_address(host, port = 7624):
    addresses.remove(host + ':' + str(port))


def add_clients():
    #: add all of the clients in client list.
    for a in addresses:
        host, port = a.split(':')
        client = Winclient(host, int(port))
        clients.append(client)


def take_image_with_one_client(client, time, temperature, binning, address):
    #: set the base properties.
    print('start capturing')
    try:
        ccd = client.get_device('SBIG CCD')
    except Exception as e:
        print(e)
        print('Couldn\'t connect to', address, 'server.')
        return
    print('hello darkness my old friend')
    ccd.configure(image_directory=image_path + str(address) + '/')
    print('configured')
    ccd.set_binning(binning[0], binning[1])
    print('binned')
    ccd.set_temperature(temperature)
    print('temp set')
    file_names.append(ccd.take_image(time))


@click.command()
@click.option('--time', type=float, help='exposure time of image')
@click.option('--temperature', type=float, help='temperature of CCD for image')
@click.option('--binning', type=(float, float), help='binning of CCD for image')
@click.option('--interval', type=float, help='interval between images')
@click.option('--count', type=int, help='number of images to take')
def capturer_cli(time, temperature, binning, interval, count):
    file.close()
    ccd_time, ccd_temp, ccd_bin = time, temperature, binning
    add_clients()
    for i in range(count):
        threads = []
        for enum, client in enumerate(clients):
            address = addresses[enum]
            t = threading.Thread(target=take_image_with_one_client, args=(client, ccd_time, ccd_temp, ccd_bin, address))
            threads.append(t)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        if not i == count - 1:
            print('Waiting', interval, 'seconds.')
            sleep(interval)
    return (file_names)


def capturer(time, temperature, binning, interval, count):
    file.close()
    ccd_time, ccd_temp, ccd_bin = time, temperature, binning
    add_clients()
    for i in range(count):
        threads = []
        for enum, client in enumerate(clients):
            address = addresses[enum]
            t = threading.Thread(target=take_image_with_one_client, args=(client, ccd_time, ccd_temp, ccd_bin, address))
            threads.append(t)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        if not i == count - 1:
            print('Waiting', interval, 'seconds.')
            sleep(interval)
    return (file_names)
