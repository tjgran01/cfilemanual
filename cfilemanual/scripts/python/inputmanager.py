import re

class InputManager(object):
    """Class with methods for sanitizing user input."""
    def __init__(self):
        pass


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
            else:
                print("That's not a valid answer, bud.")


    def get_numerical_input(prompt, num_options, extra_option=None):
        """Sanatizes user input when chosing between multiple options.
        Args:
            prompt: the question displayed to the user
            num_options: the amount of options the user has to chode between.
            extra_options: optional arguement if there is an extra argument
            outside of 'num_options'
        Returns:
            ans: sanitized answer to the prompt."""
        while True:
            print(prompt)
            try:
                ans = int(input("> "))
            except ValueError:
                print("You need to enter a number.")
                continue
            if not extra_option:
                if re.match(f"^[1-{str(num_options)}]$", str(ans)):
                    return ans
                else:
                    print("That's not a valid answer.")
            else:
                if re.match(f"^[1-{str(num_options)}]$", str(ans)):
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
            except FileNotFoundError:
                print("Hmm. Looks like that is not a valid filepath. Try again.")
                print("To quit the program enter control-c.")
