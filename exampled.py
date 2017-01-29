import time
import daemon
try:
    from daemon.pidfile import PIDLockFile
except:
    from daemon.pidlockfile import PIDLockFile


def run():
    count = 0
    # Daemons usually have an 'endless' like loop someplace. This one is not
    # doing much but keeping track of how many loop iterations have been made.
    while True:
        count += 1
        print("Loop: {}".format(count))
        time.sleep(30)


if __name__ == '__main__':

    # The pid file allows us to find the process id of the daemon after it has
    # been launched and backrouned.
    if pidfile:
        pid_ctx = PIDLockFile(pidfile)
    else:
        pid_ctx = None

    # Daemons that conform to good unix style close all file handlers and
    # change directory to the root of the filesystem before forking.
    # Here, we are telling python daemon not to close standard out or standard
    # error. This is usefull for beingable to print debuging info.
    files_preserve = [sys.stdout, sys.stderr]

    # You can run in the 'foreground' or 'detach'.
    # - When running in the foreground (detach = False) you can stop the
    #   process with Ctrl-C.
    # - When detaching, you will be returned to the command prompt right away.
    # You'll need to look at the pid file or process list to find the process.
    # Then use the kill command to stop it `kill $(cat mypidfile)`
    detatch = False

    with daemon.DaemonContext(pidfile=pid_ctx, detach_process=detatch, files_preserve=files_preserve):
        run()
