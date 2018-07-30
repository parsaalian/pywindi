from pywindi.winclient import Winclient
import threading
import click


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


def take_image_with_one_client(client, temprature, exposure_time):
    ccd = client.get_device_by_name('SBIG CCD')
    ccd.configure(image_directory=image_path)
    ccd.set_temperature(temprature)
    ccd.take_image(exposure_time)


#@click.command()
#@click.argument('exposure_time')
#@click.argument('temprature')
def cli(exposure_time=10, temprature=5):
    add_clients()
    threads = []
    for client in clients:
        t = threading.Thread(target=take_image_with_one_client, args=(client, temprature, exposure_time))
        threads.append(t)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    cli()
