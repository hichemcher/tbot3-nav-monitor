import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/cheriet/tbot3_ws/install/tbot3_nav_monitor'
