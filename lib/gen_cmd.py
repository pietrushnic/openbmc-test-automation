#!/usr/bin/env python

r"""
This module provides command execution functions such as cmd_fnc and cmd_fnc_u.
"""

import sys
import subprocess
import collections

import gen_print as gp
import gen_valid as gv
import gen_misc as gm

robot_env = gp.robot_env

if robot_env:
    import gen_robot_print as grp


def cmd_fnc(cmd_buf,
            quiet=None,
            test_mode=None,
            debug=0,
            print_output=1,
            show_err=1,
            return_stderr=0):

    r"""
    Run the given command in a shell and return the shell return code and the
    output.

    Description of arguments:
    cmd_buf                         The command string to be run in a shell.
    quiet                           Indicates whether this function should run
                                    the print_issuing() function which prints
                                    "Issuing: <cmd string>" to stdout.
    test_mode                       If test_mode is set, this function will
                                    not actually run the command.  If
                                    print_output is set, it will print
                                    "(test_mode) Issuing: <cmd string>" to
                                    stdout.
    debug                           If debug is set, this function will print
                                    extra debug info.
    print_output                    If this is set, this function will print
                                    the stdout/stderr generated by the shell
                                    command.
    show_err                        If show_err is set, this function will
                                    print a standardized error report if the
                                    shell command returns non-zero.
    return_stderr                   If return_stderr is set, this function
                                    will process the stdout and stderr streams
                                    from the shell command separately.  It
                                    will also return stderr in addition to the
                                    return code and the stdout.
    """

    # Determine default values.
    quiet = int(gm.global_default(quiet, 0))
    test_mode = int(gm.global_default(test_mode, 0))

    if debug:
        gp.print_vars(cmd_buf, quiet, test_mode, debug)

    err_msg = gv.svalid_value(cmd_buf)
    if err_msg != "":
        raise ValueError(err_msg)

    if not quiet:
        gp.pissuing(cmd_buf, test_mode)

    if test_mode:
        if return_stderr:
            return 0, "", ""
        else:
            return 0, ""

    if return_stderr:
        err_buf = ""
        stderr = subprocess.PIPE
    else:
        stderr = subprocess.STDOUT

    sub_proc = subprocess.Popen(cmd_buf,
                                bufsize=1,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=stderr)
    out_buf = ""
    if return_stderr:
        for line in sub_proc.stderr:
            err_buf += line
            if not print_output:
                continue
            if robot_env:
                grp.rprint(line)
            else:
                sys.stdout.write(line)
    for line in sub_proc.stdout:
        out_buf += line
        if not print_output:
            continue
        if robot_env:
            grp.rprint(line)
        else:
            sys.stdout.write(line)
    if print_output and not robot_env:
        sys.stdout.flush()
    sub_proc.communicate()
    shell_rc = sub_proc.returncode
    if shell_rc != 0 and show_err:
        err_msg = "The prior command failed.\n" + gp.sprint_var(shell_rc, 1)
        if not print_output:
            err_msg += "out_buf:\n" + out_buf

        if robot_env:
            grp.rprint_error_report(err_msg)
        else:
            gp.print_error_report(err_msg)

    if return_stderr:
        return shell_rc, out_buf, err_buf
    else:
        return shell_rc, out_buf


def cmd_fnc_u(cmd_buf,
              quiet=None,
              debug=None,
              print_output=1,
              show_err=1,
              return_stderr=0):

    r"""
    Call cmd_fnc with test_mode=0.  See cmd_fnc (above) for details.

    Note the "u" in "cmd_fnc_u" stands for "unconditional".
    """

    return cmd_fnc(cmd_buf, test_mode=0, quiet=quiet, debug=debug,
                   print_output=print_output, show_err=show_err,
                   return_stderr=return_stderr)


def parse_command_string(command_string):

    r"""
    Parse a bash command-line command string and return the result as a
    dictionary of parms.

    This can be useful for answering questions like "What did the user specify
    as the value for parm x in the command string?".

    This function expects the command string to follow the following posix
    conventions:
    - Short parameters:
      -<parm name><space><arg value>
    - Long parameters:
      --<parm name>=<arg value>

    The first item in the string will be considered to be the command.  All
    values not conforming to the specifications above will be considered
    positional parms.  If there are multiple parms with the same name, they
    will be put into a list (see illustration below where "-v" is specified
    multiple times).

    Description of argument(s):
    command_string                  The complete command string including all
                                    parameters and arguments.

    Sample input:

    robot_cmd_buf:                                    robot -v
    OPENBMC_HOST:dummy1 -v keyword_string:'Set Auto Reboot  no' -v
    lib_file_path:/home/user1/git/openbmc-test-automation/lib/utils.robot -v
    quiet:0 -v test_mode:0 -v debug:0
    --outputdir='/home/user1/status/children/'
    --output=dummy1.Auto_reboot.170802.124544.output.xml
    --log=dummy1.Auto_reboot.170802.124544.log.html
    --report=dummy1.Auto_reboot.170802.124544.report.html
    /home/user1/git/openbmc-test-automation/extended/run_keyword.robot

    Sample output:

    robot_cmd_buf_dict:
      robot_cmd_buf_dict[command]:                    robot
      robot_cmd_buf_dict[v]:
        robot_cmd_buf_dict[v][0]:                     OPENBMC_HOST:dummy1
        robot_cmd_buf_dict[v][1]:                     keyword_string:Set Auto
        Reboot no
        robot_cmd_buf_dict[v][2]:
        lib_file_path:/home/user1/git/openbmc-test-automation/lib/utils.robot
        robot_cmd_buf_dict[v][3]:                     quiet:0
        robot_cmd_buf_dict[v][4]:                     test_mode:0
        robot_cmd_buf_dict[v][5]:                     debug:0
      robot_cmd_buf_dict[outputdir]:
      /home/user1/status/children/
      robot_cmd_buf_dict[output]:
      dummy1.Auto_reboot.170802.124544.output.xml
      robot_cmd_buf_dict[log]:
      dummy1.Auto_reboot.170802.124544.log.html
      robot_cmd_buf_dict[report]:
      dummy1.Auto_reboot.170802.124544.report.html
      robot_cmd_buf_dict[positional]:
      /home/user1/git/openbmc-test-automation/extended/run_keyword.robot
    """

    # We want the parms in the string broken down the way bash would do it,
    # so we'll call upon bash to do that by creating a simple inline bash
    # function.
    bash_func_def = "function parse { for parm in \"${@}\" ; do" +\
        " echo $parm ; done ; }"

    rc, outbuf = cmd_fnc_u(bash_func_def + " ; parse " + command_string,
                           quiet=1, print_output=0)
    command_string_list = outbuf.rstrip("\n").split("\n")

    command_string_dict = collections.OrderedDict()
    ix = 1
    command_string_dict['command'] = command_string_list[0]
    while ix < len(command_string_list):
        if command_string_list[ix].startswith("--"):
            key, value = command_string_list[ix].split("=")
            key = key.lstrip("-")
        elif command_string_list[ix].startswith("-"):
            key = command_string_list[ix].lstrip("-")
            ix += 1
            try:
                value = command_string_list[ix]
            except IndexError:
                value = ""
        else:
            key = 'positional'
            value = command_string_list[ix]
        if key in command_string_dict:
            if type(command_string_dict[key]) is str:
                command_string_dict[key] = [command_string_dict[key]]
            command_string_dict[key].append(value)
        else:
            command_string_dict[key] = value
        ix += 1

    return command_string_dict
