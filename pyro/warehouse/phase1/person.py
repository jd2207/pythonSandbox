from __future__ import print_function
import sys

if sys.version_info < (3, 0):
    input = raw_input


class Person(object):
    def __init__(self, name):
        self.name = name

    def visit(self, warehouse):
        print("Hello " + self.name +". The warehouse contains:", warehouse.list_contents())
        self.deposit(warehouse)
        self.retrieve(warehouse)
        print("Goodbye " + self.name +". The warehouse now contains:", warehouse.list_contents())

    def deposit(self, warehouse):
        item = input("Type a thing you want to store (or empty): ").strip()
        if item:
            warehouse.store(self.name, item)

    def retrieve(self, warehouse):
        item = input("Type something you want to take (or empty): ").strip()
        if item:
            warehouse.take(self.name, item)
