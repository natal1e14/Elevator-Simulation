"""CSC148 Assignment 1 - People and Elevators

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains classes for the two "basic" entities in this simulation:
people and elevators. We have provided basic outlines of these two classes
for you; you are responsible for implementing these two classes so that they
work with the rest of the simulation.

You may NOT change any existing attributes, or the interface for any public
methods we have provided. However, you can (and should) add new attributes,
and of course you'll have to implement the methods we've provided, as well
as add your own methods to complete this assignment.

Finally, note that Person and Elevator each inherit from a kind of sprite found
in sprites.py; this is to enable their instances to be visualized properly.
You may not change sprites.py, but are responsible for reading the documentation
to understand these classes, as well as the abstract methods your classes must
implement.
"""
from __future__ import annotations
from typing import List
from sprites import PersonSprite, ElevatorSprite


class Elevator(ElevatorSprite):
    """An elevator in the elevator simulation.

    Remember to add additional documentation to this class docstring
    as you add new attributes (and representation invariants).

    === Attributes ===
    passengers: A list of the people currently on this elevator
    current_floor: the floor the elevator is currently on
    max_pass: the maximum number of passengers the elevator can have

    === Representation invariants ===
        max_pass > 0

    """
    passengers: List[Person]
    current_floor: int
    max_pass: int

    def __init__(self, passengers: List[Person], el_max: int) -> None:
        ElevatorSprite.__init__(self)
        self.current_floor = 1
        self.max_pass = el_max
        self.passengers = passengers

    #Calculates how full an elevator is
    def fullness(self) -> int:

        return (len(self.passengers)*1.0)/self.max_pass


class Person(PersonSprite):
    """A person in the elevator simulation.

    === Attributes ===
    start: the floor this person started on
    target: the floor this person wants to go to
    wait_time: the number of rounds this person has been waiting for

    === Representation invariants ===
    start >= 1
    target >= 1
    wait_time >= 0
    """
    start: int
    target: int
    wait_time: int

    def __init__(self, start: int, target: int) -> None:


        self.start = start
        self.target = target
        self.wait_time = 0
        PersonSprite.__init__(self)




    def get_anger_level(self) -> int:
        """Return this person's anger level."""

        if self.wait_time <= 2:
            return 0
        elif 3 <= self.wait_time <= 4:
            return 1
        elif 5 <= self.wait_time <= 6:
            return 2
        elif 7 <= self.wait_time <= 8:
            return 3
        else:
            return 4



if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['sprites'],
        'max-nested-blocks': 4,
        'max-attributes': 12,
        'disable': ['R0201']
    })
