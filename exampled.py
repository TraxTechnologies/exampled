import argparse
import time
import sys
import os
import daemon
try:
    from daemon.pidfile import PIDLockFile
except:
    from daemon.pidlockfile import PIDLockFile

argparser = argparse.ArgumentParser('exampled.py', 'Simple Example Python Daemon')
argparser.add_argument(
    '--pidfile', default='exampled.pid', help='When forking, write the process id to this file'
)
argparser.add_argument(
    '--detach', action='store_true', default=False, help='When forking, write the process id to this file'
)
argparser.add_argument(
    '--quiet', action='store_true', default=False, help='Do not preserve stdin and stdout'
)
argparser.add_argument(
    '--logfile', default='exampled.log', help='Write to this file'
)

def run(logfile):
    count = 0
    # Daemons usually have an 'endless' like loop someplace. This one is not
    # doing much but keeping track of how many loop iterations have been made.
    while True:
        count += 1
        print("Loop: {}".format(count))
        with open(logfile, 'a') as fp:
            fp.write('Loop: {}\n'.format(count))
        time.sleep(30)


if __name__ == '__main__':
    args = argparser.parse_args()
    working_dir = os.getcwd()
    options = {
        'pidfile': None,
        'detach_process': args.detach,
        'stderr': None,
        'stdout': None,
        'working_directory': '/',
    }


    # The pid file allows us to find the process id of the daemon after it has
    # been launched and backrouned.
    if args.pidfile:
        options['pidfile'] = PIDLockFile(args.pidfile)

    # Daemons that conform to good unix style close all file handlers and
    # change directory to the root of the filesystem before forking.
    # For testing, stay in the current working directory
    options['working_directory'] = os.getcwd()

    if not args.quiet:
        # Here, we are telling python daemon not to close standard out or standard
        # error. This is usefull for beingable to print debuging info.
        options['stdout'] = sys.stdout
        options['stderr'] = sys.stderr
        # If we had opened some other files we'd need to add them here or they
        # will be closed.
        files_preserve = []

    # You can run in the 'foreground' or 'detach'.
    # - When running in the foreground (detach = False) you can stop the
    #   process with Ctrl-C.
    # - When detaching, you will be returned to the command prompt right away.
    #   You'll need to look at the pid file or process list to find the process.
    #   Then use the kill command to stop it `kill $(cat mypidfile)`
    if args.detach:
        options['detach'] = True

    print("Launching daemon...")
    with daemon.DaemonContext(**options):
        run(args.logfile)
