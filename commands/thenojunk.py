# file SacredSeed/commands/thenojunk.py

from evennia import default_cmds
from evennia import utils
from random import randint
import re
# from evennia import typeclasses


class CmdWoDRoll(default_cmds.MuxCommand):
    """
    Theno's WoD Roller

    Usage:
      wod <# of dice>[=<target(s)>]

    Current state: Returns a bunch of d10s rolled to the user.
    """

    key = "wod"

    # some globals
    MAX_POOL = 100
    DIFFICULTY = 8
    DIFFICULTY_CHANCE = 10
    DEFAULT_AGAIN = 10

    def func(self):
        """
        wod <value>[=<targets>]

        Returns:
            Doesn't return anything
        """
        caller = self.caller

        # NO ARGS -> return with error
        if not self.lhs:
            caller.msg("Usage: wod <pool>[ = <targets>]")
            return

        # DETERMINE TARGETS: spaces or commas?
        if self.rhs:
            targets = self.build_search_list(self.rhs)
            if not targets:
                return
        else:
            targets = [caller]

        # BUILD POOL (# of dice to roll)
        text_input = re.sub(r' +', ' ', self.lhs)
        pool, pretty_input = self.build_pool(text_input)
        if pool > self.MAX_POOL:
            self.caller.msg(f"{pool} is too many dice. I can only roll {self.MAX_POOL}.")
            return

        # ROLL THE POOL (`pool` dice)
        result = self.roll_pool(pool)

        # SUCCESS COUNTER
        difficulty = self.DIFFICULTY if pool > 0 else self.DIFFICULTY_CHANCE

        # this thing is apparently called "list comprehension" and it's cool
        success_values = [x for x in result if x >= difficulty]
        successes = len(success_values)

        message = self.build_output(pool, difficulty, result, successes, pretty_input)
        message += f"\n>> Targets: {targets}"

        self.caller.msg(message)

    def build_search_list(self, targets_string):
        """

        Args:
            targets_string: space- or comma-delimited list of names
        (see if we can't manage '...' as valid way to deal with spaces - unlikely)

        Returns:
            list[] of objects found

        """
        caller = self.caller
        here = caller.location

        if "," in targets_string:
            delimiter = ","
        else:
            delimiter = " "

        targets = [target.strip() for target in targets_string.split(delimiter)]  # remove spaces around each element
        targets = [caller.search(target) for target in set(targets)]  # search each element, reporting misfires
        targets = [target for target in targets if target]  # remove empty elements

        if here in targets:
            targets.remove(here)
            targets += here.contents

        targets = list(set().union(*[targets]))  # get rid of redundant targets

        return targets

    def build_pool(self, input_text):
        """
        How many dice do we need to roll?
        Also build the output-ready version of input_text (may split this to another function)

        Args:
            input_text: <item>[ <operator> <item>]..., e.g., a + b - c + d

        Returns:
            total number of dice to roll, pretty version of the input
        """
        # re.split() includes elements found
        # uses + or - as an item to split on
        # e.g. 'a + b - c + d' --> '['a', '+', 'b', '-', 'c', '+', 'd']
        pool = re.split(r'\s*([+-])\s*', input_text)

        total_pool = 0
        sign = 1
        pretty_pool = ''
        operator = ''

        for element in pool:
            if element == "+":
                sign = 1
                operator = " + "
            elif element == "-":
                sign = -1
                operator = " - "
            else:
                try:
                    element = int(element)
                    value, pretty_text = self.calculate_number(element)
                    total_pool += value * sign
                    pretty_pool += operator + pretty_text
                except ValueError:
                    value, pretty_text = self.calculate_trait(element)
                    total_pool += value * sign
                    pretty_pool += operator + pretty_text

        return total_pool, pretty_pool

    def calculate_number(self, value):
        "validate a single integer value; probably needs to do nothing"
        return value, str(value)

    def calculate_trait(self, trait):
        """
        Presently does nothing; returns 0.

        Depending on `trait` format:
        * trait - Pull trait from character sheet
        * name:trait - Pull trait from someone else's sheet, with permissions

        Args:
            trait: Statistic on a character sheet or other known stat

        Returns:
            number of dice this represents, prettified text of 'trait'
        """
        trait = f"|x[{trait}]|n"
        return 0, trait

    def roll_pool(self, pool):
        """
        Roll <pool> number of d10s.

        Args:
            pool: Number of dice to roll

        Returns:
            total number of dice to roll
        """
        result = []
        if pool > 0:
            for die in range(pool):
                result += self.roll_die()
            return result
        else:
            return self.roll_die()

    def roll_die(self, again=DEFAULT_AGAIN):
        """
        Roll 1d10. Roll another on a result of >= `again`

        Args:
            again: What value of the roll means "roll another die"

        Returns:
            list[] of die/dice results
        """
        die = randint(1, 10)
        if (die >= again) and not (again == 0):
            return [die] + self.roll_die(again)
        else:
            return [die]

    def build_output(self, pool, difficulty, result, successes, pretty_input):
        """
        Just how do we show the output? With care.

        Args:
            pool: number of dice
            difficulty: # at which or higher a success is counted
            result: list[] of dice rolled, in order
            successes: how many of those were successes?
            pretty_input: pretty version of what the player entered (lhs)
            ## targets: list[] of objects to tell
        Returns:
            the final text to output
        """

        pretty_result = []

        for x in result:
            if x >= difficulty:
                pretty_result.append(f"|h{x}|n")
            else:
                pretty_result.append(f"|x{x}|n")
        pretty_result = ' '.join(pretty_result)

        message = f"Rolling: {pretty_input} |x({pool} dice)|n\nResult: {pretty_result} "
        if successes >= 1:
            message += "|G(success)|n"
        else:
            message += "|R(failure)|n"

        return message
