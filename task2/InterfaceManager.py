import json
from typing import List, Dict

import requests
from marshmallow import EXCLUDE

from argument_parser import arg_pars
from data_type import Interface
from utils import get_logger

# Argument parser
args = arg_pars()

# Logger
logger = get_logger(log_path=args.log_path, log_name=args.log_name, log_level=args.log_level)


def protocol(ssl):
    if ssl:
        return 'https'
    else:
        return 'http'


def url_check(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
    except Exception as e:
        raise SystemExit(e)


# Setting URL
set_url = f'{protocol(args.ssl)}://{args.host}:{args.port}/get-all-interfaces'
url_check(set_url)


class InterfaceManager:
    def __init__(self, api_url=set_url):
        self.api_url = api_url
        self.interface_schema = Interface.schema()
        self.parsed_data = self._get_all_interfaces()

    def _get_all_interfaces(self) -> List[Interface]:
        response = requests.get(self.api_url)
        parsed_interfaces = self.interface_schema.loads(json_data=response.text, many=True, unknown=EXCLUDE)
        return parsed_interfaces

    def analyze(self) -> Dict:
        enabled_count = 0
        types = {}
        missing_ipv4, missing_ipv6 = [], []
        for data in self.parsed_data:
            if not data.ip_address_1.address:
                missing_ipv4.append(data.name)
            if not data.ip_address_2.address:
                missing_ipv6.append(data.name)
            if data.enabled:
                enabled_count += 1
            types[data.type] = types.get(data.type, 0) + 1
        no_ip_addresses = list(set(missing_ipv4).intersection(missing_ipv6))
        logger.info(f'A total of {len(self.parsed_data)} interfaces were obtained and from that:')
        for key in types:
            logger.info(f'{types[key]} interfaces of type {key}.')
        logger.info(f'{enabled_count} enabled interfaces.')
        logger.info(f'{len(missing_ipv4)} interfaces with missing ipv4 address: {missing_ipv4}')
        logger.info(f'{len(missing_ipv6)} interfaces with missing ipv4 address: {missing_ipv6}')
        logger.info(f'{len(no_ip_addresses)} interfaces with no ip addresses: {no_ip_addresses}')
        logg_dict = {'interface_count': len(self.parsed_data), 'enabled_interfaces': enabled_count,
                     'interfaces_types': types, 'interfaces_with_missing_ips': {
                'missing:ipv4': {'count': len(missing_ipv4), 'interfaces': missing_ipv4},
                'missing:ipv6': {'count': len(missing_ipv6), 'interfaces': missing_ipv6},
                'missing_completely_both': {'count': len(no_ip_addresses), 'interfaces': [no_ip_addresses]}}}
        return logg_dict

    def write_all_data(self) -> None:
        with open('output_folder/output_data.json', 'w') as f:
            f.write(self.interface_schema.dumps(self.parsed_data, many=True, ensure_ascii=False, indent=4))
        with open('output_folder/logg_data.json', 'w') as f:
            json.dump(self.analyze(), f, ensure_ascii=False, indent=4)


def main():
    interface_manager = InterfaceManager()
    interface_manager.write_all_data()


if __name__ == "__main__":
    main()
