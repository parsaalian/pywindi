from windi.winclient import Winclient
import threading

class Imagetaker:
    image_path = '/home/dimm/Desktop/images/'
    address = ['localhost:7624']
    clients = []

    def add_address(self, host, port):
        self.address.append(host + ':' + str(port))


    def add_clients(self):
        for a in self.address:
            host, port = a.split(':')
            client = Winclient(host, int(port))
            self.clients.append(client)


    def take_image_with_one_client(self, client, temprature, exposure_time):
        ccd = client.get_device_by_name('SBIG CCD')
        ccd.configure(image_directory=self.image_path)
        ccd.set_temperature(temprature)
        ccd.take_image(exposure_time)


    def take_image(self, temprature=5, exposure_time=10):
        self.add_clients()
        threads = []
        for client in self.clients:
            t = threading.Thread(target=self.take_image_with_one_client, args=(client, temprature, exposure_time))
            threads.append(t)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
