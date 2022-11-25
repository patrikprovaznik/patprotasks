from argparse import ArgumentParser, Namespace


def arg_pars() -> Namespace:
    parser = ArgumentParser(description="Loading arguments.")
    parser.add_argument('--debug', action='store_true', help='print debug message')
    parser.add_argument('--ssl', action='store_true', help='Set protocol for URL.')
    parser.add_argument('-ho', '--host', dest='host', metavar='HOST', help='Set host for URL.', required=True)
    parser.add_argument('-po', '--port', dest='port', metavar='PORT', help='Set port for URL.', required=True)
    parser.add_argument('-lf', '--l_fold', dest='logs_fold', metavar='LOG_FOLD',
                        help="Set name of folder for logs, e.g. logs/", required=False, default="logs/")
    parser.add_argument('-lp', '--l_path', dest='log_path', metavar='LOG_PATH',
                        help="Set path with name for .log file, e.g. /home/Documents/<log_name>.log.", required=False,
                        default="logs/logger_2.log")
    parser.add_argument('-ll', '--level', dest='log_level', metavar='LOG_LEVEL', help="Set logging level",
                        required=False, default="logging.INFO")
    parser.add_argument('-of', '--output', dest='out_fold', metavar='OUT_FOLD',
                        help="Set name of output folder for output files, e.g. output_folder.", required=False,
                        default="output_folder/")
    parser.add_argument('-od', '--out_data', dest='out_data', metavar='OUT_DATA',
                        help="Set name for output data file in .json format, e.g. output_data.json.", required=False,
                        default="output_data.json")
    parser.add_argument('-ld', '--log_data', dest='log_data', metavar='LOG_DATA',
                        help="Set name for log data file in .json format, e.g. log_data.json.", required=False,
                        default="log_data.json")

    return parser.parse_args()
