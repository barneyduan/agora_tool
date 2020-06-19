# -*- coding: utf-8 -*-

import re
import os
import os.path
import subprocess
import fcntl
import select
import errno
import chardet
import json

class bcolors:
    """
    Terminal Colors
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def make_async(fd):
    """
    Helper function to add the O_NONBLOCK flag to a file descriptor
    """
    fcntl.fcntl(fd, fcntl.F_SETFL, fcntl.fcntl(
        fd, fcntl.F_GETFL) | os.O_NONBLOCK)

def read_async(fd):
    """
    Helper function to read some data from a file descriptor, ignoring EAGIN
    errors
    """
    try:
        return fd.read()
    except IOError as e:
        if e.errno != errno.EAGAIN:
            raise e
    else:
        return ''


def try_to_decode(s):
    encoding = chardet.detect(s)['encoding']
    if encoding:
        return s.decode(encoding)
    else:
        return s.decode()

def merge_and_decode(vec):
    out = b''.join([item for item in vec if item])
    if out:
        return try_to_decode(out)
    else:
        return ''

def run_command(cmd, cwd=None, silence=False, shell=False):
    """
    Run command, get stdout and stderr
    """
    if not silence:
        print("Run command:", cmd, ", with cwd:", cwd)
    if shell==True:
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    else:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)

    make_async(process.stdout)
    make_async(process.stderr)

    stdout = []
    stderr = []
    return_code = None

    while True:
        # Wait data to become avaliable
        select.select([process.stdout, process.stderr], [], [])

        # Try reading some data from each
        stdout_piece = read_async(process.stdout)
        stderr_piece = read_async(process.stderr)

        if stdout_piece and not silence:
            print(try_to_decode(stdout_piece), end='')
        if stderr_piece and not silence:
            print(bcolors.WARNING + try_to_decode(stderr_piece) + bcolors.ENDC, end='')

        stdout.append(stdout_piece)
        stderr.append(stderr_piece)

        return_code = process.poll()

        if return_code != None:
            if return_code != 0 and not silence:
                print(bcolors.FAIL + "Script error..." + bcolors.ENDC)

            return merge_and_decode(stdout), merge_and_decode(stderr), return_code


