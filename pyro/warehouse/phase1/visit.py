# This is the code that runs this example.

# from warehouse import Warehouse
from person import Person
import Pyro4

# warehouse = Warehouse()

# "remote" case
uri = raw_input("Enter the uri of the warehouse: ").strip()
warehouse = Pyro4.Proxy(uri)

name = raw_input("Who are you?").strip()

visitor = Person(name)
visitor.visit(warehouse)
