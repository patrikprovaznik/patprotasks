import argparse


def arg_pars():
    parser = argparse.ArgumentParser(description="Loading arguments.")
    parser.add_argument('--debug', action='store_true', help='print debug message')
    parser.add_argument('--ssl', action='store_true', help='Set protocol for URL.')
    parser.add_argument('-ho', '--host', dest='host', metavar='HOST', help='Set host for URL.', required=True)
    parser.add_argument('-po', '--port', dest='port', metavar='PORT', help='Set port for URL.', required=True)
    parser.add_argument('-pt', '--path', dest='log_path', metavar='LOG_PATH',
                        help="Set path with name for .log file, e.g. /home/Documents/<log_name>.log.", required=False,
                        default="logs/logger_2.log")
    parser.add_argument('-ll', '--level', dest='log_level', metavar='LOG_LEVEL', choices={'logging.INFO',
                                                                                          'logging.DEBUG',
                                                                                          'logging.WARNING',
                                                                                          'logging.ERROR'},
                        help="Set logging level", required=False, default="logging.INFO")
    return parser.parse_args()
