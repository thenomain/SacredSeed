# file SacredSeed/commands/thenojunk.py

from evennia import default_cmds

# import re
from random import randint


class CmdWoDRoll(default_cmds.MuxCommand):
    """
    Theno's WoD Roller

    Usage:
      wod <# of dice>

    Current state: Returns a bunch of d10s rolled to the user.
    """

    key = "wod"

    def __init__(self):
        """
        Set up some command settings. Must be global. Must be a better way to do this.
        """
        global CONST_MAX_POOL
        CONST_MAX_POOL = 100  # max number of dice that can be sent to the final "pool" roller.

    def func(self):
        "roll things"

        if not self.args:
            self.caller.msg("Nothing passed")
            return

        pool = 0
        value = self.lhs

        # is `value` a number or trait?
        try:
            value = int(value)  # valid for things like "+1" and "-100"
            pool += self.calculate_number(value)
        except ValueError:
            pool += self.calculate_trait(value)

        if pool > CONST_MAX_POOL:
            self.caller.msg("Too many dice.")
            return 0

        # ROLL
        self.caller.msg("> # of dice ---> %i" % pool)
        result = self.roll_pool(pool)
        self.caller.msg("> result --> %r" % result)

        # SUCCESS COUNTER
        # this thing is apparently called "list comprehension" and it's cool
        success_values = [x for x in result if x >= 8]
        successes = len(success_values)
        self.caller.msg("> successes --> %r (%r)" % (success_values, successes))

        # OUTPUT
        # target = self.rhs
        # message = "Rolling " + str(value)
        result_pretty = []
        for x in result:
            if x >= 8:
                result_pretty.append(f"|h{x}|n")
            else:
                result_pretty.append(f"|x{x}|n")
        result_pretty = ' '.join(result_pretty)

        # Darren's Idea: ' '.join(f|{"h" if x > 8 else "X"}{x}|n" for x in result])

        message = f"Rolling: {value}\nResults: {result_pretty} "
        if successes >= 1:
            message += "|G(success)|n"
        else:
            message += "|R(failure)|n"

        self.caller.msg(message)

    def calculate_number(self, value):
        "validate a single integer value"
        self.caller.msg("> number: %s" % value)
        return value

    def calculate_trait(self, trait):
        "validate a single string; assume trait and take apart"
        self.caller.msg("> trait: %s" % trait)
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


# if 10 in dice_roll_list:
#     do_dice_stuff()

# list1 = list.append(*list2) <-- * unpacks the list :: [a,b,c] -> a,b,c