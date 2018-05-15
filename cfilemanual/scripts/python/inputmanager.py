import re
import sys

class InputManager(object):
    """Class with methods for sanitizing user input."""
    def __init__(self):
        pass


    def clean_exit():
        """Exits the program without calling a traceback or raising a Keyboard
        Inturupt.
        """
        print("Closing program ... ...")
        sys.exit()


    def get_yes_or_no(prompt):
        """Sanatizes user input for yes or no questions.

        Args:
            prompt: the question displayed to the user.
        Returns:
            Bool - True for yes answer, False for No Answer."""

        while True:
            print(prompt)
            ans = input("> ")
            if ans[0].lower() == "y":
                return True
            elif ans[0].lower() == "n":
                return False
            elif ans == "QUIT" or ans == "KILL":
                clean_exit()
            else:
                print("That's not a valid answer, bud.")


    def get_numerical_input(prompt, num_options, extra_option=None):
        """Sanatizes user input when chosing between multiple options.

        Args:
            prompt(str): the question displayed to the user
            num_options(int): the amount of options the user has to choose
            between.
            extra_options: optional arguement if there is an extra argument
            outside of 'num_options'
        Returns:
            ans: sanitized answer to the prompt."""
        while True:
            print(prompt)
            try:
                ans = input("> ")
                if ans == "QUIT" or ans == "KILL":
                    clean_exit()
                ans = int(ans)
            except ValueError:
                print("You need to enter a number.")
                continue

            if not extra_option:
                if re.match(f"^([1-9]|[1-9][0-{str(num_options)[1]}])$",
                            str(ans)):
                    return ans
                else:
                    print(str(num_options))
                    print("That's not a valid answer.")
            else:
                if re.match(f"^([1-9]|[1-9][0-{str(num_options)[1]}])$",
                            str(ans)):
                    return ans
                if ans == extra_option:
                    return ans
                else:
                    print("That's not a valid answer.")


    def get_valid_fpath(prompt):
        """Ensures that a file exists at the filepath a user enters.

        Args:
            prompt: the question displayed to the user.
        Returns:
            fpath(str): location of the file.
        """

        while True:
            print(prompt)
            fpath = input("> ")
            try:
                with open (fpath) as in_file:
                    data = in_file.read()
                return fpath
            except (FileNotFoundError, IsADirectoryError) as error:
                print("Hmm. Looks like that is not a valid filepath. Try again.")
                print("To quit the program enter control-c.")


    def get_variable_name(prompt):
        while True:
            print(prompt)
            ans = input("> ")
            if len(ans) > 0 and " " not in ans and not ans[0].isnumeric():
                return ans
            print("Hmm. That doesn't appear to be a valid variable name."
                  "Variable names must be more than 0 characters, and can't"
                  " contain whitespace.")
