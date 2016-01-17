"""
Module that defines all algorithm-related types.
"""
import re


NORTH = 0
WEST = 1
SOUTH = 2
EAST = 3


class Rover(object):
    """
    The main rover class.
    """

    def __init__(self, upper_right_x, upper_right_y, x, y, direction):
        """
        Initializes a rover.

        :param upper_right_x: the upper right X-coordinate for the plateau.
        :param upper_right_y: the upper right Y-coordinate for the plateau.
        :param x: the current rover X-coordinate position.
        :param y: the current rover Y-coordinate position.
        :param direction: the current rover direction it is facing (NORTH, EAST. SOUTH, WEST).
        """
        self.upper_right_x = upper_right_x
        self.upper_right_y = upper_right_y
        self.position_x = x
        self.position_y = y
        self.direction = direction

    def left_rotate(self):
        """
        Rotates the rover 90 degrees left.
        """
        if self.direction == EAST:
            self.direction = NORTH
        else:
            self.direction += 1

    def right_rotate(self):
        """
        Rotates the rover 90 degrees right.
        """
        if self.direction == NORTH:
            self.direction = EAST
        else:
            self.direction -= 1

    def move_forward(self):
        """
        Moves the rover one step forward.
        """
        position_x, position_y = self.position_x, self.position_y
        if self.direction == NORTH:
            position_y += 1
        elif self.direction == SOUTH:
            position_y -= 1
        elif self.direction == EAST:
            position_x += 1
        elif self.direction == WEST:
            position_x -= 1

        if (position_x < 0 or position_y < 0):
            raise ValueError('Cannot go anywhere behind (0,0)')
        if (position_x > self.upper_right_x or position_y > self.upper_right_y):
            raise ValueError('Cannot go anywhere further than (%s,%s)' % (
                self.upper_right_x, self.upper_right_y))

        self.position_x = position_x
        self.position_y = position_y

    def get_position(self):
        """
        Gets the current position.

        :returns: a 3-tuple (x, y, direction)
        :rtype: tuple
        """
        return (self.position_x, self.position_y, self.direction)


class RoversHandler(object):
    """
    A rover handler, that receives input from outside and processes it accordingly.
    """
    PLATEAU_UPPER_RIGHT_REGEX = re.compile(r'^(?P<x>\d+) (?P<y>\d+)$')
    ROVER_POSITION_REGEX = re.compile(r'^(?P<x>\d+) (?P<y>\d+) (?P<facing>[NSEW])$')
    ROVER_INSTRUCTIONS_REGEX = re.compile(r'^(?P<instructions>[LMR]+)$')

    PLATEAU_UPPER_RIGHT_TYPE = 0
    ROVER_POSITION_TYPE = 1
    ROVER_INSTRUCTIONS_TYPE = 2

    DIRECTION_MAPPING = {'N': NORTH, 'S': SOUTH, 'E': EAST, 'W': WEST}

    def __init__(self):
        self.rovers = []
        self.last_line = None
        self.upper_right_x = None
        self.upper_right_y = None

    def process_line(self, line):
        """
        Processes a line from outside and interprets it accordingly, also making sure of its
        correctness.

        :param line: a input line.
        :type line: str
        """
        match = None
        if self.last_line is None:
            match = self.PLATEAU_UPPER_RIGHT_REGEX.match(line)
            type_ = self.PLATEAU_UPPER_RIGHT_TYPE
        elif self.last_line in (self.PLATEAU_UPPER_RIGHT_TYPE, self.ROVER_INSTRUCTIONS_TYPE):
            match = self.ROVER_POSITION_REGEX.match(line)
            type_ = self.ROVER_POSITION_TYPE
        elif self.last_line == self.ROVER_POSITION_TYPE:
            match = self.ROVER_INSTRUCTIONS_REGEX.match(line)
            type_ = self.ROVER_INSTRUCTIONS_TYPE

        if match is None:
            # no match, error
            raise ValueError('Invalid line or unexpected line type: "%s"' % line)
        else:
            match = match.groupdict()

        if type_ == self.PLATEAU_UPPER_RIGHT_TYPE:
            # defining plateau upper right coordinates
            self.upper_right_x, self.upper_right_y = int(match['x']), int(match['y'])

        elif type_ == self.ROVER_POSITION_TYPE:
            # setting up a new rover with given initial coordinates
            x, y = int(match['x']), int(match['y'])
            direction = self.DIRECTION_MAPPING[match['facing']]
            rover = Rover(self.upper_right_x, self.upper_right_y, x, y, direction)
            self.rovers.append(rover)

        elif type_ == self.ROVER_INSTRUCTIONS_TYPE:
            # giving instructions to a rover
            rover = self.rovers[-1]
            for move in match['instructions']:
                if move == 'L':
                    rover.left_rotate()
                elif move == 'R':
                    rover.right_rotate()
                elif move == 'M':
                    rover.move_forward()

        self.last_line = type_

    def get_output_lines(self):
        """
        Returns all output lines expected from the latest processing.

        :rtype: list
        :returns: a list of lines (each of them a string)
        """
        response = []
        DIRECTION_REVERSE_MAPPING = dict((v, k) for k, v in self.DIRECTION_MAPPING.iteritems())
        for rover in self.rovers:
            x, y, position = rover.get_position()
            response.append('%s %s %s' % (x, y, DIRECTION_REVERSE_MAPPING[position]))
        return response
