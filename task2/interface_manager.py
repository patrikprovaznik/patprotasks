import json
import os
from argparse import Namespace
from collections import defaultdict
from logging import Logger
from typing import List, Dict

import requests
from marshmallow import EXCLUDE

from argument_parser import arg_pars
from data_type import Interface
from utils import get_logger


def protocol(ssl: str) -> str:
    return 'https' if ssl else 'http'


class InterfaceManager:
    def __init__(self, api_url: str, logger: Logger, args: Namespace) -> None:
        self._api_url = api_url
        self._interface_schema = Interface.schema()
        self._logger = logger
        self._args = args

    def _get_all_interfaces(self) -> List[Interface]:
        try:
            response = requests.get(self._api_url)
            response.raise_for_status()
            parsed_interfaces = self._interface_schema.loads(json_data=response.text, many=True, unknown=EXCLUDE)
            return parsed_interfaces
        except Exception as e:
            self._logger.exception("Error: it is not possible to get data from the specified URL.")
            raise SystemExit(e)

    def analyze(self) -> Dict:
        parsed_data = self._get_all_interfaces()
        enabled_count = 0
        types = defaultdict(int)
        missing_ipv4, missing_ipv6 = [], []
        for data in parsed_data:
            if not data.ip_address_1.address:
                missing_ipv4.append(data.name)
            if not data.ip_address_2.address:
                missing_ipv6.append(data.name)
            if data.enabled:
                enabled_count += 1
            types[data.type] += 1
        no_ip_addresses = list(set(missing_ipv4).intersection(missing_ipv6))
        self._logger.info(f'A total of {len(parsed_data)} interfaces were obtained and from that:')
        for key in types:
            self._logger.info(f'{types[key]} interfaces of type {key}.')
        self._logger.info(f'{enabled_count} enabled interfaces.')
        self._logger.info(f'{len(missing_ipv4)} interfaces with missing ipv4 address: {missing_ipv4}')
        self._logger.info(f'{len(missing_ipv6)} interfaces with missing ipv6 address: {missing_ipv6}')
        self._logger.info(f'{len(no_ip_addresses)} interfaces with no ip addresses: {no_ip_addresses}')
        logg_dict = {'interface_count': len(parsed_data), 'enabled_interfaces': enabled_count,
                     'interfaces_types': types, 'interfaces_with_missing_ips': {
                'missing:ipv4': {'count': len(missing_ipv4), 'interfaces': missing_ipv4},
                'missing:ipv6': {'count': len(missing_ipv6), 'interfaces': missing_ipv6},
                'missing_completely_both': {'count': len(no_ip_addresses), 'interfaces': [no_ip_addresses]}}}
        return logg_dict

    def write_all_data(self) -> None:
        parsed_data = self._get_all_interfaces()
        output_folder = self._args.out_fold
        os.makedirs(output_folder, exist_ok=True)
        with open(output_folder + self._args.out_data, 'w') as f:
            f.write(self._interface_schema.dumps(parsed_data, many=True, ensure_ascii=False))
        with open(output_folder + self._args.log_data, 'w') as f:
            json.dump(self.analyze(), f, ensure_ascii=False)
