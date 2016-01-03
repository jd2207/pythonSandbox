from __future__ import print_function
import Pyro4


class Warehouse(object):
    def __init__(self):
        self.contents = ["chair", "bike", "flashlight", "laptop", "couch"]

    def list_contents(self):
        return self.contents

    def take(self, visitor, item):
        self.contents.remove(item)
        self.printRecord(visitor, item, False)

    def store(self, visitor, item):
        self.contents.append(item)
        self.printRecord(visitor, item, True)

    def printRecord(self, visitor, item, store=True):
        text = 'stored' if store else 'took'
        print( ("{0} " + text + " the {1}.").format(visitor, item))
        print('Contents now are: ', self.list_contents())
          
      

def main():
    warehouse = Warehouse()
    Pyro4.Daemon.serveSimple(
            {
                warehouse: "example.warehouse"
            },
            ns = False)

if __name__=="__main__":
    main()