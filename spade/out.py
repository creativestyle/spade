from __future__ import print_function
import sys


def fmt_color(msg, color_nr):
    return '\033[0;%dm%s\033[0m' % (color_nr, msg)


def fmt_error(msg):
    return fmt_color(msg, 31)


def fmt_success(msg):
    return fmt_color(msg, 32)


def fmt_warn(msg):
    return fmt_color(msg, 33)


def fmt_info(msg):
    return fmt_color(msg, 34)


def fmt_em(msg):
    return fmt_color(msg, 35)


def print_success(msg):
    print(fmt_success('\n * ' + msg))


def print_warn(msg):
    print(fmt_warn(msg))


def print_error(msg):
    print(fmt_error(msg), file=sys.stderr)


def print_header(name):
    # print('\n%s\n%s\n' % (name, fmt_em(len(name) * '=')))
    print('\n %s %s\n' % (fmt_em('*'), name))


def print_step(msg):
    print(fmt_em('   --> ') + msg)


def fail(msg):
    print_error('\n ' + msg)
    exit(1)
