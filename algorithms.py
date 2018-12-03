"""CSC148 Assignment 1 - Algorithms

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module Description ===

This file contains two sets of algorithms: ones for generating new arrivals to
the simulation, and ones for making decisions about how elevators should move.

As with other files, you may not change any of the public behaviour (attributes,
methods) given in the starter code, but you can definitely add new attributes
and methods to complete your work here.

See the 'Arrival generation algorithms' and 'Elevator moving algorithsm'
sections of the assignment handout for a complete description of each algorithm
you are expected to implement in this file.
"""
import csv
from enum import Enum
import random
from typing import Dict, List, Optional

from entities import Person, Elevator


###############################################################################
# Arrival generation algorithms
###############################################################################
class ArrivalGenerator:
    """An algorithm for specifying arrivals at each round of the simulation.

    === Attributes ===
    max_floor: The maximum floor number for the building.
               Generated people should not have a starting or target floor
               beyond this floor.
    num_people: The number of people to generate, or None if this is left
                up to the algorithm itself.

    === Representation Invariants ===
    max_floor >= 2
    num_people is None or num_people >= 0
    """
    max_floor: int
    num_people: Optional[int]

    def __init__(self, max_floor: int, num_people: Optional[int]) -> None:
        """Initialize a new ArrivalGenerator.

        Preconditions:
            max_floor >= 2
            num_people is None or num_people >= 0
        """
        self.max_floor = max_floor
        self.num_people = num_people

    def generate(self, round_num: int) -> Dict[int, List[Person]]:
        """Return the new arrivals for the simulation at the given round.

        The returned dictionary maps floor number to the people who
        arrived starting at that floor.

        You can choose whether to include floors where no people arrived.
        """
        raise NotImplementedError


class RandomArrivals(ArrivalGenerator):
    """Generate a fixed number of random people each round.

    Generate 0 people if self.num_people is None.

    For our testing purposes, this class *must* have the same initializer header
    as ArrivalGenerator. So if you choose to to override the initializer, make
    sure to keep the header the same!

    Hint: look up the 'sample' function from random.
    """

    def __init__(self, max_floor: int, num_people: Optional[int]) -> None:

        ArrivalGenerator.__init__(self, max_floor, num_people)

    def generate(self, round_num: int) -> Optional[Dict[int, List[Person]]]:
        """Randomly generates num_people for the given round_num

        Returns a list containing the floors in the simulation and
        the people (if any) that have just arrived on that floor
        """

        #If the number of people to generate is not None
        if self.num_people is not None:

            arrivals = {}

            #Add a key to arrivals for every floor starting at 1 to max_floor
            for i in range(1, self.max_floor+1):
                neww = {i: []}
                arrivals.update(neww)

            pop = []

            #populate pop with all possible floor numbers
            for j in range(1, self.max_floor + 1):
                pop.append(j)

            #generate num_people people
            for i in range(0, self.num_people):

                neww = random.sample(pop, 2)
                start = neww[0]
                target = neww[1]
                new = Person(start, target)
                arrivals[start].append(new)
            return arrivals
        else:
            return None


class FileArrivals(ArrivalGenerator):
    """Generate arrivals from a CSV file.

    Attributes:
        arrivals: a dictionary containing the arrivals to be generated in
            every round
    """
    arrivals: Dict[int, Person]

    def __init__(self, max_floor: int, filename: str) -> None:
        """Initialize a new FileArrivals algorithm from the given file.

        The num_people attribute of every FileArrivals instance is set to None,
        since the number of arrivals depends on the given file.

        Precondition:
            <filename> refers to a valid CSV file, following the specified
            format and restrictions from the assignment handout.
        """
        ArrivalGenerator.__init__(self, max_floor, None)
        self.arrivals = {}

        # We've provided some of the "reading from csv files" boilerplate code
        # for you to help you get started.
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)

            for line in reader:

                ln = int(line[0])
                self.arrivals[ln] = []

                #instantiate all people for the simulation
                for i in range(1, len(line)-1, 2):
                    new_person = Person(int(line[i]), int(line[i+1]))

                    self.arrivals[ln].append(new_person)
                    #self.arrivals[ln].append(int(line[i+1]))



    def generate(self, round_num: int) -> Dict[int, Person]:
        """Generates the new arrivals for the given round_num
        from self.arrivals"""

        new_arrivals = {}

        # Add a key to arrivals for every floor starting at 1 to max_floor
        for i in range(1, self.max_floor+1):
            neww = {i: []}
            new_arrivals.update(neww)

        #If there are people to be generated this round according to the file
        if round_num in self.arrivals:

            for i in range(0, len(self.arrivals[round_num])):

                new_person = self.arrivals[round_num][i]
                new_arrivals[new_person.start].append(new_person)

        return new_arrivals





###############################################################################
# Elevator moving algorithms
###############################################################################
class Direction(Enum):
    """
    The following defines the possible directions an elevator can move.
    This is output by the simulation's algorithms.

    The possible values you'll use in your Python code are:
        Direction.UP, Direction.DOWN, Direction.STAY
    """
    UP = 1
    STAY = 0
    DOWN = -1


class MovingAlgorithm:
    """An algorithm to make decisions for moving an elevator at each round.
    """
    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:
        """Return a list of directions for each elevator to move to.

        As input, this method receives the list of elevators in the simulation,
        a dictionary mapping floor number to a list of people waiting on
        that floor, and the maximum floor number in the simulation.

        Note that each returned direction should be valid:
            - An elevator at Floor 1 cannot move down.
            - An elevator at the top floor cannot move up.
        """
        raise NotImplementedError


class RandomAlgorithm(MovingAlgorithm):
    """A moving algorithm that randomly determines which direction an
    elevator should move (Up, down, or stay on the same floor
    """


    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:

        """Takes the number of elevators in the simulation, a dictionary
        of the people waiting and the max floor, and returns a list containing
        the direction each elevator should move.

        Determines the direction each elevator should move randomly"""
        directions = []
        for elevator in elevators:

            #If the elevator is on the first floor, either go up or stay
            if elevator.current_floor == 1:
                move = random.randint(0, 1)

            #if the elevator is on the max floor, either stay or go down
            elif elevator.current_floor == max_floor:
                move = random.randint(-1, 0)

            #otherwise, it can move up, down or stay
            else:
                move = random.randint(-1, 1)
            elevator.current_floor += move

            #Append the appropriate command to directions
            if move == 0:
                directions.append(Direction.STAY)
            elif move == 1:
                directions.append(Direction.UP)
            else:
                directions.append(Direction.DOWN)
        return directions












class PushyPassenger(MovingAlgorithm):
    """A moving algorithm that preferences the first passenger on each elevator.

    If the elevator is empty, it moves towards the *lowest* floor that has at
    least one person waiting, or stays still if there are no people waiting.

    If the elevator isn't empty, it moves towards the target floor of the
    *first* passenger who boarded the elevator.
    """

    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:

        """Takes the number of elevators in the simulation, a dictionary
        of the people waiting and the max floor, and returns a list containing
        the direction each elevator should move

        Determines the direction each elevator in the simulation should move
        based on the PushyPassenger description above"""

        direction = []

        #For every elevator in the simulation
        for elevator in elevators:

            #If the elevator has passengers
            if len(elevator.passengers) > 0:

                #Take the first passenger (the one that has been on longest)
                passenger = elevator.passengers[0]

                #If the passenger's target is above the current floor, go up
                if passenger.target > elevator.current_floor:
                    move = Direction.UP
                    elevator.current_floor += 1

                #If the passenger's target is below the current floor, go down
                else:
                    move = Direction.DOWN
                    elevator.current_floor += -1

            #If the elevator is empty
            else:

                p_waiting = False #Becomes T if people are waiting
                for i in range(1, max_floor+1):
                    length = len(waiting[i])
                    difference = elevator.current_floor - i

                    # if someone is waiting on floor i, and i is < current floor
                    if length > 0 and difference > 0:
                        p_waiting = True
                        move = Direction.DOWN
                        elevator.current_floor += -1
                        break

                    #if someone is waiting at floor i and i is > current floor
                    elif difference < 0 < length:
                        move = Direction.UP
                        p_waiting = True
                        elevator.current_floor += 1
                        break

                #If no one is waiting in the simulation, elevator stays
                if p_waiting is False:
                    move = Direction.STAY
            direction.append(move)
        return direction


class ShortSighted(MovingAlgorithm):
    """A moving algorithm that preferences the closest possible choice.

    If the elevator is empty, it moves towards the *closest* floor that has at
    least one person waiting, or stays still if there are no people waiting.

    If the elevator isn't empty, it moves towards the closest target floor of
    all passengers who are on the elevator.

    In this case, the order in which people boarded does *not* matter.
    """

    def move_elevators(self,
                       elevators: List[Elevator],
                       waiting: Dict[int, List[Person]],
                       max_floor: int) -> List[Direction]:

        """Takes the number of elevators in the simulation, a dictionary
        of the people waiting and the max floor, and returns a list containing
        the direction each elevator should move

        Determines the direction each elevator in the simulation should move
        based on the ShortSighted description above"""

        direction = []
        waiters = False

        #Checks to see if there are any people waiting anywhere in the sim
        for j in range(1, len(waiting)+1):
            if len(waiting[j]) > 0:
                waiters = True
                break


        for elevator in elevators:

            #a value guaranteed to be further than any other value
            closest = max_floor*3


            #if the elevator has no passengers
            if len(elevator.passengers) <= 0 and waiters:

                for i in range(1, len(waiting)+1):

                    #if floor i is closer than closest
                    if abs(closest-elevator.current_floor) >= \
                            abs(i-elevator.current_floor) and \
                            len(waiting[i]) > 0:
                        closest = i

                    #if floor i is equidistiance to closest but lower
                    elif abs(closest-elevator.current_floor) == \
                            abs(i-elevator.current_floor) \
                            and len(waiting[i]) > 0\
                            and closest-elevator.current_floor > 0:

                        closest = i

            #if no one is waiting and elevator is empty
            elif len(elevator.passengers) <= 0 and not waiters:
                closest = elevator.current_floor


            #if the elevator has passenger(s)
            else:

                closest = elevator.passengers[0].target

                for passenger in elevator.passengers:

                    #if passenger's target is closer than closest
                    if abs(closest - elevator.current_floor) > abs(
                            passenger.target - elevator.current_floor):
                        closest = passenger.target

                    #if passenger's target is closer than closest and lower
                    elif abs(closest - elevator.current_floor) == abs(
                            passenger.target - elevator.current_floor)\
                            and passenger.target - elevator.current_floor < 0:
                        closest = passenger.target

            #if the closest floor is lower than the current floor, go down
            if elevator.current_floor - closest > 0:
                direction.append(Direction.DOWN)
                elevator.current_floor += -1

            #if closest is above current floor, go up
            elif elevator.current_floor - closest < 0:
                direction.append(Direction.UP)
                elevator.current_floor += 1

            #Otherwise, don't move
            else:
                direction.append(Direction.STAY)

        return direction



if __name__ == '__main__':
    # Don't forget to check your work regularly with python_ta!
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['__init__'],
        'extra-imports': ['entities', 'random', 'csv', 'enum'],
        'max-nested-blocks': 4,
        'max-attributes': 12,
        'disable': ['R0201']
    })
