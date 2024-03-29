# PyQt5Singleton
A simple singleton implementation to work with PyQt5

## Installation
Using pip:

```sh
$ pip install PyQt5Singleton
```

or clone this repo, install dependencies and run install:

```sh
$ git clone https://github.com/jazzycamel/PyQt5Singleton.git
$ cd PyQt5Singleton
$ pip install -r requirements.txt
$ python setup.py install
```

## Usage
```python
from PyQt5.QtCore import QObject, pyqtSlot, pyqtProperty
from PyQt5Singleton import Singleton

class MyObject(QObject, metaclass=Singleton):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self._x=0

    def x(self): return self._x

    @pyqtSlot(int)
    def setX(self, x): self._x=x

    x=pyqtProperty(int, x, setX)

if __name__=="__main__":
    print(MyObject().x)
    MyObject().x=1
    print(MyObject().x)
```
