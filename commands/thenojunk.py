# file SacredSeed/commands/thenojunk.py

# Assure that our command class is the default set by the game
from django.conf import settings
from evennia.utils import utils

COMMAND_DEFAULT_CLASS = utils.class_from_module(settings.COMMAND_DEFAULT_CLASS)

# <Griatch> You could make a ticket for trying to add that line to evennia.init.py (the flat API).
#   I couldn't promise it would work well to do so but it would be pretty neat to be able to offer
#   the default like that I suppose.

from random import randint
import re
from thenocode.finders import build_targets_list
from thenocode.formaters import header, footer, divider


class CmdWoDRoll(COMMAND_DEFAULT_CLASS):
    """
    Theno's WoD Roller

    Usage:
      wod <# of dice>[=<target(s)>]

    Current state: Returns a bunch of d10s rolled to the target(s).
    """

    key = "wod"

    # some globals
    MAX_POOL = 100
    DIFFICULTY = 8
    DIFFICULTY_CHANCE = 10  # difficulty on a chance-die
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

        # DETERMINE TARGETS
        if self.rhs:
            targets = build_targets_list(self, self.rhs, False)
            if not targets:
                caller.msg("No valid targets. Roll aborted.")
                return
        else:
            targets = [caller.location]

        # BUILD POOL (# of dice to roll)
        text_input = re.sub(r' +', ' ', self.lhs)
        pool, pretty_input = self.build_pool(text_input)
        if pool > self.MAX_POOL:
            caller.msg(f"{pool} is too many dice. I can only roll {self.MAX_POOL}.")
            return

        # ROLL THE POOL (`pool` dice)
        result = self.roll_pool(pool)

        # SUCCESS COUNTER
        difficulty = self.DIFFICULTY if pool > 0 else self.DIFFICULTY_CHANCE

        # this thing is apparently called "list comprehension" and it's cool
        success_values = [x for x in result if x >= difficulty]
        successes = len(success_values)

        # OUTPUT RESULT
        message = self.build_output(pool, difficulty, result, successes, pretty_input)
        # message += f"\n[Targets: {self.prettify_targets(targets)}]"
        # caller.msg(self.styled_header("test built-in header"))
        caller.msg(header(self, "test header"))

        for target in targets:
            if caller in target.contents:
                target.msg_contents(message)
            else:
                target.msg(message)

        caller.msg(footer(self, self.prettify_targets(targets)))
        # caller.msg(self.styled_footer(self.prettify_targets(targets)))

    def build_pool(self, input_text):
        """
        How many dice do we need to roll?
        Also build the output-ready version of input_text

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
        """
        Args:
            value: number of dice to roll

        Returns:
            number of dice to roll (i.e. 'value'), prettified text version of 'value'
        """
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

        for r in result:
            if r >= difficulty:
                pretty_result.append(f"|h{r}|n")
            else:
                pretty_result.append(f"|x{r}|n")
        pretty_result = ' '.join(pretty_result)

        message = f"Rolling: {pretty_input} |x({pool} dice)|n\nResult: {pretty_result} "
        if successes >= 1:
            message += "|G(success)|n"
        else:
            message += "|R(failure)|n"

        return message

    def prettify_targets(self, targets):
        """
        Args:
            targets: Objects being shown the output

        Returns:
            some pretty text like 'here'
        """
        message = []

        for t in targets:
            if t == self.caller.location:
                message.append("Here")
            else:
                message.append(str(t))

        message = ", ".join(message)

        return message
