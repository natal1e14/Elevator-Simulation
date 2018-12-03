"""CSC148 Assignment 1 - Simulation

=== CSC148 Fall 2018 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This contains the main Simulation class that is actually responsible for
creating and running the simulation. You'll also find the function `sample_run`
here at the bottom of the file, which you can use as a starting point to run
your simulation on a small configuration.

Note that we have provided a fairly comprehensive list of attributes for
Simulation already. You may add your own *private* attributes, but should not
remove any of the existing attributes.
"""
# You may import more things from these modules (e.g., additional types from
# typing), but you may not import from any other modules.
from typing import Dict, List, Any

import algorithms
from entities import Person, Elevator
from visualizer import Visualizer


class Simulation:
    """The main simulation class.

    === Attributes ===
    arrival_generator: the algorithm used to generate new arrivals.
    elevators: a list of the elevators in the simulation
    moving_algorithm: the algorithm used to decide how to move elevators
    num_floors: the number of floors
    visualizer: the Pygame visualizer used to visualize this simulation
    waiting: a dictionary of people waiting for an elevator
             (keys are floor numbers, values are the list of waiting people)
    num_rounds: the number of rounds the simulation should run for
    _waitt: stores the amount of time it took people to reach their target floor
    __people_completed: the number of people that reached their target floor
    _total_people: the total number of people generated in the simulation

    === Representation Invariants ===
        elevators > 0
        num_floors > 0
        num_rounds > 0
    """
    arrival_generator: algorithms.ArrivalGenerator
    elevators: List[Elevator]
    moving_algorithm: algorithms.MovingAlgorithm
    num_floors: int
    visualizer: Visualizer
    waiting: Dict[int, List[Person]]
    num_rounds: int
    __people_completed: int
    _total_people: int
    _waitt: List[int]

    def __init__(self,
                 config: Dict[str, Any]) -> None:
        """Initialize a new simulation using the given configuration."""

        # Initialize the visualizer.
        # Note that this should be called *after* the other attributes
        # have been initialized.


        self.num_floors = config['num_floors']
        self.elevators = []
        self.waiting = {}
        for i in range(1, self.num_floors+1):
            self.waiting[i] = []
        for i in range(0, config['num_elevators']):
            self.elevators.append(Elevator([], config['elevator_capacity']))

        self.arrival_generator = config['arrival_generator']
        self.moving_algorithm = config['moving_algorithm']

        self.visualizer = Visualizer(self.elevators, self.num_floors,
                                     config['visualize'])

        self.num_rounds = 0
        self.__people_completed = 0
        self._waitt = []
        self._total_people = 0

    ############################################################################
    # Handle rounds of simulation.
    ############################################################################
    def run(self, num_rounds: int) -> Dict[str, Any]:
        """Run the simulation for the given number of rounds.

        Return a set of statistics for this simulation run, as specified in the
        assignment handout.

        Precondition: num_rounds >= 1.

        Note: each run of the simulation starts from the same initial state
        (no people, all elevators are empty and start at floor 1).
        """
        self.num_rounds = num_rounds
        for i in range(num_rounds):
            self.visualizer.render_header(i)

            # Stage 1: generate new arrivals
            self._generate_arrivals(i)

            # Stage 2: leave elevators
            self._handle_leaving()

            # Stage 3: board elevators
            self._handle_boarding()

            # Stage 4: move the elevators using the moving algorithm
            self._move_elevators()

            # Update anger of all peoples
            self._update_anger()

            # Pause for 1 second
            self.visualizer.wait(1)

        return self._calculate_stats()

    def _generate_arrivals(self, round_num: int) -> None:
        """Generate and visualize new arrivals."""

        arrivals = self.arrival_generator.generate(round_num)

        #If there are new arrivals, add the new arrivals self.waiting
        if arrivals is not None:
            for i in range(1, len(arrivals)+1):
                current = self.waiting[i]
                self.waiting[i] = current + arrivals[i]
                self._total_people += len(arrivals[i])
            self.visualizer.show_arrivals(arrivals)


    def _handle_leaving(self) -> None:
        """Handle people leaving elevators."""

        for elevator in self.elevators:

            for passenger in elevator.passengers:

                #if a passenger has reached their target floor
                if passenger.target == elevator.current_floor:
                    self.__people_completed += 1
                    self._waitt.append(passenger.wait_time)
                    passenger.start = passenger.target
                    elevator.passengers.remove(passenger)
                    self.visualizer.show_disembarking(passenger, elevator)


    def _handle_boarding(self) -> None:

        """Handle boarding of people and visualize."""
        for i in range(1, self.num_floors+1):
            lst = self.waiting[i]
            for elevator in self.elevators:
                self._update_elevator(elevator, i, lst)

    def _update_anger(self) -> None:

        """Update the wait_time of people who haven't
        reached their target floor yet"""

        #Update anger of people waiting on floors
        for i in range(1, len(self.waiting)+1):
            for person in self.waiting[i]:
                person.wait_time += 1

        #Update anger of people on elevators
        for elevator in self.elevators:
            for person in elevator.passengers:
                person.wait_time += 1

    def _update_elevator(self, elevator: Elevator, floor: int,
                         lst: List[Person]) -> None:

        """Add passengers to the elevator"""

        #If the elevator is on the specified floor and not at max capacity
        if elevator.current_floor == floor and \
                  len(elevator.passengers) < elevator.max_pass:

            #While the elevator is not at max capacity and there are people on
            #the floor
            while (len(elevator.passengers) < elevator.max_pass) and (
                    len(lst) > 0):
                elevator.passengers.append(lst[0])
                self.visualizer.show_boarding(lst[0], elevator)
                lst.remove(lst[0])

    def _move_elevators(self) -> None:
        """Move the elevators in this simulation.

        Use this simulation's moving algorithm to move the elevators.
        """
        moves = self.moving_algorithm.move_elevators(self.elevators,
                                                     self.waiting,
                                                     self.num_floors)
        self.visualizer.show_elevator_moves(self.elevators, moves)

    ############################################################################
    # Statistics calculations
    ############################################################################
    def _calculate_stats(self) -> Dict[str, int]:
        """Report the statistics for the current run of this simulation.
        """


        #If no one reached their target floor
        if self.__people_completed == 0:
            max_wait = -1
            min_wait = -1
            avg_wait = -1

        #if people reached their target floor
        else:
            min_wait = min(self._waitt)
            max_wait = max(self._waitt)

            #Calculate the average wait time
            summ = 0
            for i in range(len(self._waitt)):
                summ += self._waitt[i]
            avg_wait = summ//len(self._waitt)


        return {
            'num_iterations': self.num_rounds,
            'total_people': self._total_people,
            'people_completed': self.__people_completed,
            'max_time': max_wait,
            'min_time': min_wait,
            'avg_time': avg_wait
        }


def sample_run() -> Dict[str, int]:
    """Run a sample simulation, and return the simulation statistics."""
    config = {
        'num_floors': 6, #check
        'num_elevators': 3, #check
        'elevator_capacity': 3, #check
        'num_people_per_round': 2,
        # Random arrival generator with 6 max floors and 2 arrivals per round.
        'arrival_generator': algorithms.FileArrivals(6,"sample_arrivals.csv"),
        'moving_algorithm': algorithms.ShortSighted(),
        'visualize': True,
        'max-attributes': 12,
        'disable': ['R0201']
    }

    sim = Simulation(config)
    stats = sim.run(10)
    return stats


if __name__ == '__main__':
    # Uncomment this line to run our sample simulation (and print the
    # statistics generated by the simulation).
    print(sample_run())
    #
    # import python_ta
    # python_ta.check_all(config={
    #     'extra-imports': ['entities', 'visualizer', 'algorithms', 'time'],
    #     'max-nested-blocks': 4,
    #     'max-attributes': 12,
    #     'disable': ['R0201']
    # })
    #sample_run()
