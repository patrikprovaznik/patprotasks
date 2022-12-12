from configparser import ConfigParser

from argument_parser import arg_pars
from interface_manager import protocol, InterfaceManager
from utils import get_logger


def main(**kwargs) -> None:
    # config
    conf = ConfigParser()
    conf.read(kwargs.get('conf_path'))
    # Logger
    logger = get_logger(log_path=kwargs.get('log_path', conf['Interface_manager']['log_path_2']), log_name=__name__,
                        log_level=kwargs.get('log_level', conf['General']['log_level']),
                        logs_fold=kwargs.get('logs_fold', conf['General']['logs_dir']))
    # Setting URL
    set_url = f'{protocol(kwargs.get("ssl"))}://{kwargs.get("host")}:{kwargs.get("port")}/get-all-interfaces'

    interface_manager = InterfaceManager(set_url, logger, kwargs, conf)
    interface_manager.write_all_data()


if __name__ == "__main__":
    # Argument parser
    args = arg_pars()
    main(**vars(args))
