# WINDI

Windi Project is a wrapper for PyIndi library that automates many functionalities with simple interface.
It is a package for python and the commands for terminal will be available in future versions.

## Installation

Use pip (recommended, but not yet)

```
pip3 install windi
```


Alternatively download [a release](https://gitlab.com/parsaalian0/windi/-/archive/master/windi-master.zip), extract it and run

```
python3 setup.py install
```


### Prerequisites

For the above installation to work, you need to have installed from your distribution repositories the following packages: libindi and pyindi-client.

For installing libindi

```
sudo apt-add-repository ppa:mutlaqja/ppa
sudo apt-get update
sudo apt-get install indi-full
sudo apt-get install swig libz3-dev libcfitsio-dev libnova-dev
```

For installing python pyindi-client:

```
pip3 install --user --install-option="--prefix=" pyindi-client
sudo -H pip3 install --system pyindi-client
```

If any errors occurred during the installation, download [pyindi-client release](https://github.com/jochym/pyindi-client/tree/master/pip/pyindi-client), extract it and run

```
python3 setup.py install
```

## Built With

* [libindi](https://github.com/indilib/indi) - The Astronomical Instrumentation Control.
* [pyindi-client](https://github.com/jochym/pyindi-client/tree/master/pip/pyindi-client) - An INDI Client Python API.

## Authors

* **Parsa Alian** - *Initial work* - [parsaalian0](https://gitlab.com/parsaalian0)
* **Emad Salehi** - [emad_salehi](https://gitlab.com/emad_salehi)

## License

This project is licensed under the MIT License.
