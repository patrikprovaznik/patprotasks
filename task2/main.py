from argument_parser import arg_pars
from utils import get_logger
from interface_manager import protocol, InterfaceManager


def main() -> None:
    # Argument parser
    args = arg_pars()

    # Logger
    logger = get_logger(log_path=args.log_path, log_name=__name__, log_level=args.log_level, logs_fold=args.logs_fold)

    # Setting URL
    set_url = f'{protocol(args.ssl)}://{args.host}:{args.port}/get-all-interfaces'

    interface_manager = InterfaceManager(set_url, logger, args)
    interface_manager.write_all_data()


if __name__ == "__main__":
    main()
