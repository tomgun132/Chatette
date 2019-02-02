"""
Module `chatette.cli.interactive_commands.execute_command`.
Contains the strategy class that represents the interactive mode command
`execute` which opens a file containing a bunch of commands and executes them.
"""

import io

from chatette.cli.interactive_commands.command_strategy import CommandStrategy, \
                                                               REDIRECTION_SYM, \
                                                               REDIRECTION_APPEND_SYM
from chatette.cli.terminal_writer import TerminalWriter, RedirectionType


class ExecuteCommand(CommandStrategy):
    def __init__(self, command_str):
        super(ExecuteCommand, self).__init__(command_str)

    def execute(self, facade):
        """
        Implements the command `execute` which executes each line of a file
        as if they were commands (unless they start with a double slash `//`).
        """
        if len(self.command_tokens) < 2:
            self.print_wrapper.error_log("Missing some arguments\nUsage: " +
                                        'execute <command-filepath>')
            return
        
        with io.open(self.command_tokens[1], 'r') as command_file:
            commands = [line.rstrip() for line in command_file.readlines()
                                      if not line.lstrip().startswith("//")]
        redirection_tuple = self.print_wrapper.get_redirection()
        if redirection_tuple is not None:
            (_, redirection_filepath) = redirection_tuple
            if redirection_filepath is not None:
                text_to_append = ' ' + REDIRECTION_APPEND_SYM + ' ' + redirection_filepath
                for (i, cmd) in enumerate(commands):
                    if (    REDIRECTION_APPEND_SYM not in cmd
                        and REDIRECTION_SYM not in cmd):
                        commands[i] += text_to_append
        return commands        
