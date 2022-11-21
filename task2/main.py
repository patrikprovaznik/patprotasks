from argument_parser import arg_pars
from interface_manager import protocol, InterfaceManager
from utils import get_logger


def main(**kwargs) -> None:
    # Logger
    logger = get_logger(log_path=kwargs.get('log_path', "logs/logger_2.log"), log_name=__name__,
                        log_level=kwargs.get('log_level', "logging.INFO"), logs_fold=kwargs.get('logs_fold', "logs/"))
    # Setting URL
    set_url = f'{protocol(kwargs.get("ssl"))}://{kwargs.get("host")}:{kwargs.get("port")}/get-all-interfaces'

    interface_manager = InterfaceManager(set_url, logger, kwargs)
    interface_manager.write_all_data()


if __name__ == "__main__":
    # Argument parser
    args = arg_pars()
    main(**vars(args))
