# file SacredSeed/commands/thenojunk.py

from evennia import default_cmds
# from evennia import typeclasses
# import re
from evennia import utils
from random import randint


class CmdWoDRoll(default_cmds.MuxCommand):
    """
    Theno's WoD Roller

    Usage:
      wod <# of dice>

    Current state: Returns a bunch of d10s rolled to the user.
    """

    key = "wod"

# some globals
    CONST_MAX_POOL = 100

    def func(self):
        "roll things"

        # NO ARGS -> return
        if not self.args or not self.lhs:
            self.caller.msg("Function format: wod <#>[=<targets>]")
            return

        # DETERMINE TARGETS: 'here' but no other locations
        if self.rhs:
            target = self.caller.search(self.rhs)
            if not target:
                return
        else:
            target = self.caller

#        if target.is_typeclass(Room, exact=false):  # 'false' means 'check all descendants'
        if utils.inherits_from(target, "typeclasses.rooms.Room"):  # Derrin says Griatch prefers this
            target = target.contents

        # BUILD POOL (# of dice to roll)
        value = self.lhs
        pool = 0

        # For some reason the following ValueErrors on `int(1.6)`, though `@py int(1.6)` returns 2. Huh.
        try:
            value = int(value)  # valid for things like "+1" and "-100"
            pool += self.calculate_number(value)
        except ValueError:
            pool += self.calculate_trait(value)

        if pool > self.CONST_MAX_POOL:
            self.caller.msg("Too many dice")
            return

        # ROLL THE POOL (`pool` dice)
        result = self.roll_pool(pool)
        # self.caller.msg("> # of dice ---> %i" % pool)
        # self.caller.msg("> result --> %r" % result)

        # SUCCESS COUNTER
        if pool <= 0:  # chance die
            difficulty = 10
        else:
            difficulty = 8

        # this thing is apparently called "list comprehension" and it's cool
        success_values = [x for x in result if x >= difficulty]
        successes = len(success_values)
        # self.caller.msg("> successes --> %r (%r)" % (success_values, successes))

        # OUTPUT TO TARGET
        result_pretty = []

        for x in result:
            if x >= difficulty:
                result_pretty.append(f"|h{x}|n")
            else:
                result_pretty.append(f"|x{x}|n")
        result_pretty = ' '.join(result_pretty)

        # Darren's Idea: ' '.join(f"|{"h" if x > 8 else "X"}{x}|n" for x in result])

        message = f"Rolling: {value}\nResults: {result_pretty} "
        if successes >= 1:
            message += "|G(success)|n"
        else:
            message += "|R(failure)|n"

        self.caller.msg(message)

    def calculate_number(self, value):
        "validate a single integer value; probably needs to do nothing"
        # self.caller.msg("> number: %s" % value)
        return value

    def calculate_trait(self, trait):
        "validate a single string; assume trait and take apart"
        # self.caller.msg("> trait: %s" % trait)
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
