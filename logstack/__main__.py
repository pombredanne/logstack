import os
import sys
try:
    import logstack
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    import logstack


if __name__ == '__main__':
    from logstack.parachute import main
    main()
