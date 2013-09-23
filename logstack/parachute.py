import logstack
import os
import platform
import runpy
import subprocess
import sys
import tempfile


# POSIX signal numbers
SIGNALS = {
        1: 'SIGHUP',
        2: 'SIGINT',
        3: 'SIGQUIT',
        4: 'SIGILL',
        6: 'SIGABRT',
        8: 'SIGFPE',
        9: 'SIGKILL',
        11: 'SIGSEGV',
        13: 'SIGPIPE',
        14: 'SIGALRM',
        15: 'SIGTERM',
    }


# Windows exception values
EXCS = {
        0x00000000: 'STATUS_WAIT_0',
        0x00000080: 'STATUS_ABANDONED_WAIT_0',
        0x000000C0: 'STATUS_USER_APC',
        0x00000102: 'STATUS_TIMEOUT',
        0x00000103: 'STATUS_PENDING',
        0x40000005: 'STATUS_SEGMENT_NOTIFICATION',
        0x40000015: 'STATUS_FATAL_APP_EXIT',
        0x80000001: 'STATUS_GUARD_PAGE_VIOLATION',
        0x80000002: 'STATUS_DATATYPE_MISALIGNMENT',
        0x80000003: 'STATUS_BREAKPOINT',
        0x80000004: 'STATUS_SINGLE_STEP',
        0x80000026: 'STATUS_LONGJUMP',
        0x80000029: 'STATUS_UNWIND_CONSOLIDATE',
        0xC0000005: 'STATUS_ACCESS_VIOLATION',
        0xC0000006: 'STATUS_IN_PAGE_ERROR',
        0xC0000008: 'STATUS_INVALID_HANDLE',
        0xC000000D: 'STATUS_INVALID_PARAMETER',
        0xC0000017: 'STATUS_NO_MEMORY',
        0xC000001D: 'STATUS_ILLEGAL_INSTRUCTION',
        0xC0000025: 'STATUS_NONCONTINUABLE_EXCEPTION',
        0xC0000026: 'STATUS_INVALID_DISPOSITION',
        0xC000008C: 'STATUS_ARRAY_BOUNDS_EXCEEDED',
        0xC000008D: 'STATUS_FLOAT_DENORMAL_OPERAND',
        0xC000008E: 'STATUS_FLOAT_DIVIDE_BY_ZERO',
        0xC000008F: 'STATUS_FLOAT_INEXACT_RESULT',
        0xC0000090: 'STATUS_FLOAT_INVALID_OPERATION',
        0xC0000091: 'STATUS_FLOAT_OVERFLOW',
        0xC0000092: 'STATUS_FLOAT_STACK_CHECK',
        0xC0000093: 'STATUS_FLOAT_UNDERFLOW',
        0xC0000094: 'STATUS_INTEGER_DIVIDE_BY_ZERO',
        0xC0000095: 'STATUS_INTEGER_OVERFLOW',
        0xC0000096: 'STATUS_PRIVILEGED_INSTRUCTION',
        0xC00000FD: 'STATUS_STACK_OVERFLOW',
        0xC0000135: 'STATUS_DLL_NOT_FOUND',
        0xC0000138: 'STATUS_ORDINAL_NOT_FOUND',
        0xC0000139: 'STATUS_ENTRYPOINT_NOT_FOUND',
        0xC000013A: 'STATUS_CONTROL_C_EXIT',
        0xC0000142: 'STATUS_DLL_INIT_FAILED',
        0xC00002B4: 'STATUS_FLOAT_MULTIPLE_FAULTS',
        0xC00002B5: 'STATUS_FLOAT_MULTIPLE_TRAPS',
        0xC00002C9: 'STATUS_REG_NAT_CONSUMPTION',
        0xC0000409: 'STATUS_STACK_BUFFER_OVERRUN',
        0xC0000417: 'STATUS_INVALID_CRUNTIME_PARAMETER',
        0xC0000420: 'STATUS_ASSERTION_FAILURE',
        0xC015000F: 'STATUS_SXS_EARLY_DEACTIVATION',
        0xC0150010: 'STATUS_SXS_INVALID_DEACTIVATION',
    }


def execute(args):
    if platform.system().lower().startswith('win'):
        retcode = subprocess.call(args)
        # casts to u64
        if retcode < 0:
            retcode += 2**64
        if (retcode >> 32) & 0xFFFFFFFF == 0xFFFFFFFF:
            excnum = retcode & 0xFFFFFFFF
            try:
                return EXCS[excnum], None
            except KeyError:
                return "Exception %d" % excnum, None
        else:
            return None, retcode & 0xFFFFFFFF
    else:
        process = subprocess.Popen(args)
        pid, status = os.waitpid(process.pid, 0)
        # Low byte: high bit is coredump indicator, rest is signal number
        signum = status & 0x7F
        # High byte: return code if signal number is 0
        code = (status >> 8) & 0xFF
        if signum != 0:
            try:
                return SIGNALS[signum], None
            except KeyError:
                return "Signal %d" % signum, None
        else:
            return None, code


def sub_main(args, crashlog):
    """Entry point for the wrapped process (that runs user code).
    """
    # Restores the arguments passed to the wrapper
    sys.argv = args
    if not os.path.exists(args[0]):
        sys.stderr.write("Error: %s does not exist\n" % args[0])
        sys.exit(1)
    logstack.enable_parachute(crashlog)
    runpy.run_path(args[0])


def main():
    """Entry point for the wrapper process (started by the user).
    """
    # Create a temporary log file
    handle, crashlog = tempfile.mkstemp(prefix='logstack_crashlog_')
    os.close(handle)

    # Execute sub_main in a subprocess
    status, code = execute([
            sys.executable,
            '-c',
            'from logstack.parachute import sub_main; sub_main(%r, %r)' % (
                    sys.argv[1:], crashlog)])

    # Check return code and read back log file
    # TODO
    os.remove(crashlog)
