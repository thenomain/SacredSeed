# file SacredSeed/commands/thenojunk.py

from evennia import default_cmds
# from evennia import typeclasses
import re
from evennia import utils
from random import randint


class CmdWoDRoll(default_cmds.MuxCommand):
    """
    Theno's WoD Roller

    Usage:
      wod <# of dice>[=<target(s)>]

    Current state: Returns a bunch of d10s rolled to the user.
    """

    key = "wod"

# some globals
    CONST_MAX_POOL = 100
    CONST_DIFFICULTY = 8
    CONST_DIFFICULTY_CHANCE = 10

    def func(self):
        """
        wod <value>[=<targets>]

        :return: None
        """

        # NO ARGS -> return
        if not self.lhs:
            self.caller.msg("Function format: wod <#>[=<targets>]")
            return

        # DETERMINE TARGETS: 'here' but no other locations
        if self.rhs:
            targets = self.caller.search(self.rhs)
            if not targets:
                return
        else:
            targets = self.caller

        if utils.inherits_from(targets, "typeclasses.rooms.Room"):
            targets = targets.contents

        # BUILD POOL (# of dice to roll)
        value = self.lhs
        pool = self.build_pool(self.lhs)
        if pool > self.CONST_MAX_POOL:
            self.caller.msg("Too many dice")
            return

        # ROLL THE POOL (`pool` dice)
        result = self.roll_pool(pool)

        # SUCCESS COUNTER
        difficulty = self.CONST_DIFFICULTY if pool > 0 else self.CONST_DIFFICULTY_CHANCE

        # this thing is apparently called "list comprehension" and it's cool
        success_values = [x for x in result if x >= difficulty]
        successes = len(success_values)

        # OUTPUT TO TARGETS
        result_pretty = []

        for x in result:
            if x >= difficulty:
                result_pretty.append(f"|h{x}|n")
            else:
                result_pretty.append(f"|x{x}|n")
        result_pretty = ' '.join(result_pretty)

        # Darren's Idea: ' '.join(f"|{"h" if x > difficulty else "X"}{x}|n" for x in result])

        message = f"Rolling: {value}\nResults: {result_pretty} "
        if successes >= 1:
            message += "|G(success)|n"
        else:
            message += "|R(failure)|n"

        self.caller.msg(message)

    def build_pool(self, input_text):
        """
        How many dice do we need to roll?

        Args:
            input_text: <item>[ <operator> <item>]..., e.g., a + b - c + d

        Returns:
            total number of dice to roll
        """
        # re.split() includes elements found
        # uses + or - as an item to split on
        # e.g. 'a + b - c + d' --> '['a ', '+', ' b ', '-', ' c ', '+', ' d']
        pool = re.split(r'\s*([+-])\s*', input_text)

        total_pool = 0
        sign = 1

        for element in pool:
            if element == "+":
                sign = 1
            elif element == "-":
                sign = -1
            else:
                try:
                    element = int(element)
                    total_pool += self.calculate_number(element) * sign
                except ValueError:
                    total_pool += self.calculate_trait(element) * sign

        return total_pool

    def calculate_number(self, value):
        "validate a single integer value; probably needs to do nothing"
        return value

    def calculate_trait(self, trait):
        """
        Presently does nothing; returns 0.

        Depending on `trait` format:
        * trait - Pull trait from character sheet
        * name:trait - Pull trait from someone else's sheet

        Args:
            trait: Statistic on a character sheet or other known stat

        Returns:
            number of dice this represents
        """
        return 0

    def roll_pool(self, pool):
        """
        Roll some dice.
        :param pool:Number of dice to roll; integer
        :return: list[] of dice rolled in order, including in order of rerolls
        """
        result = []
        if pool > 0:
            for die in range(pool):
                result += self.roll_die()
            return result
        else:
            return self.roll_die()

    def roll_die(self, again=10):
        """
        Roll 1d10. Roll another on a result of >= `again`
        :param again: What value of the roll means "roll another die"
        :return: list[] of die/dice results
        """
        die = randint(1, 10)
        if (die >= again) and not (again == 0):
            return [die] + self.roll_die(again)
        else:
            return [die]

    def build_output(self, **kwargs):
        """

        :param kwargs:
            rolled: pretty version of what the player entered (lhs)
            pool: number of dice
            result: pretty version of the roll
            targets: list[] of objects to tell
        :return:
        """
