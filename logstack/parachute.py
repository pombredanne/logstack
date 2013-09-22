import sys
import tempfile


def sub_main(args, crashlog):
    """Entry point for the wrapped process (that runs user code).
    """
    # TODO : set parachute mode and execute user's code


def main():
    """Entry point for the wrapper process (started by the user).
    """
    # Create a temporary log file
    handle, crashlog = tempfile.mkstemp(prefix='logstack_crashlog_')
    os.close(handle)

    # Execute sub_main in a subprocess
    retcode = subprocess.call(sys.executabe, '-c', 'from logstack.parachute import sub_main; sub_main(%r, %r)' % (sys.argv, crashlog))

    # Check return code and read back log file
    # TODO
