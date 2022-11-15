"""A collection of Commands shared across all command books."""

import config
import utils
import time
from vkeys import key_down, key_up, press


#############################
#       Shared Commands     #
#############################
class Command:
    name = 'Command Superclass'

    @utils.run_if_enabled
    def execute(self):
        """
        Prints this Command's string representation and executes its main function.
        :return:    None
        """

        print(self)
        self.main()

    def main(self):
        pass

    def __str__(self):
        """
        Returns a string representing this Command instance.
        :return:    This Command's string representation.
        """

        variables = self.__dict__
        result = f'    {self.name}'
        if len(variables) > 1:
            result += ':'
        for key, value in variables.items():
            if key != 'name':
                result += f'\n        {key}={value}'
        return result


class Goto(Command):
    """Moves config.seq_index to the index of the specified label."""

    def __init__(self, label):
        self.name = 'Goto'
        self.label = str(label)

    def main(self):
        try:
            config.seq_index = config.sequence.index(self.label)
        except ValueError:
            print(f"Label '{self.label}' does not exist.")


class Wait(Command):
    """Waits for a set amount of time."""

    def __init__(self, duration):
        self.name = 'Wait'
        self.duration = float(duration)

    def main(self):
        time.sleep(self.duration)


class Walk(Command):
    """Walks in the given direction for a set amount of time."""

    def __init__(self, direction, duration):
        self.name = 'Walk'
        self.direction = utils.validate_horizontal_arrows(direction)
        self.duration = float(duration)

    def main(self):
        key_down(self.direction)
        time.sleep(self.duration)
        key_up(self.direction)
        time.sleep(0.05)


class Fall(Command):
    """
    Performs a down-jump and then free-falls until the player exceeds a given distance
    from their starting position.
    """

    def __init__(self, distance=config.move_tolerance/2):
        self.name = 'Fall'
        self.distance = float(distance)

    def main(self):
        start = config.player_pos
        key_down('down')
        time.sleep(0.05)
        counter = 6
        while config.enabled and \
                counter > 0 and \
                utils.distance(start, config.player_pos) < self.distance:
            press('space', 1, down_time=0.1)
            counter -= 1
        key_up('down')
        time.sleep(0.1)


#################################
#       Default Commands        #
#################################
class DefaultMove(Command):
    """Undefined 'move' command for the default command book."""

    def __init__(self, x, y, adjust='False', max_steps=15):
        self.name = 'Undefined Move Command'

    def main(self):
        config.enabled = False


class DefaultAdjust(Command):
    """Undefined 'adjust' command for the default command book."""

    def __init__(self, x, y, max_steps=5):
        self.name = 'Undefined Adjust Command'

    def main(self):
        config.enabled = False


class DefaultBuff(Command):
    """Undefined 'buff' command for the default command book."""

    def __init__(self):
        self.name = 'Undefined Buff Command'

    def main(self):
        config.enabled = False
