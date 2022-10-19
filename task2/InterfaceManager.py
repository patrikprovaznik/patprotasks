import json
import logging
from dataclasses import dataclass, field
from typing import List

import marshmallow as mm
import requests
from dataclasses_json import DataClassJsonMixin, config
from marshmallow import fields, EXCLUDE

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler('output_folder/interfaces.log', mode='w')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


@dataclass
class AddressIpv4Inside(DataClassJsonMixin):
    ip: str
    netmask: str


@dataclass
class AddressIpv6Inside(DataClassJsonMixin):
    ip: str
    prefix_length: int = field(
        metadata=config(mm_field=mm.fields.Number(data_key='prefix-length')))


@dataclass
class AddressIpv4(DataClassJsonMixin):
    address: List[AddressIpv4Inside] = field(
        metadata=config(mm_field=mm.fields.List(fields.Nested(AddressIpv4Inside.schema(unknown=mm.EXCLUDE)))),
        default_factory=list)


@dataclass
class AddressIpv6(DataClassJsonMixin):
    address: List[AddressIpv6Inside] = field(
        metadata=config(mm_field=mm.fields.List(fields.Nested(AddressIpv6Inside.schema(unknown=mm.EXCLUDE)))),
        default_factory=list)


@dataclass
class Interface(DataClassJsonMixin):
    name: str
    description: str = field(metadata=config(mm_field=mm.fields.String(data_key='description', load_default=str)))
    type: str
    enabled: bool
    ip_address_1: AddressIpv4 = field(
        metadata=config(mm_field=mm.fields.Nested(AddressIpv4.schema(unknown=mm.EXCLUDE), data_key='ietf-ip:ipv4')))
    ip_address_2: AddressIpv6 = field(
        metadata=config(mm_field=mm.fields.Nested(AddressIpv6.schema(unknown=mm.EXCLUDE), data_key='ietf-ip:ipv6')))


class InterfaceManager:
    def __init__(self, url="http://127.0.0.1:5000/get-all-interfaces"):
        self.api_url = url
        self.interface_schema = Interface.schema()
        self.parsed_data = self.get_all_interfaces()

    def get_all_interfaces(self) -> List[Interface]:
        response = requests.get(self.api_url)
        parsed_interfaces = self.interface_schema.loads(json_data=response.text, many=True, unknown=EXCLUDE)
        return parsed_interfaces

    def analyze(self):
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

    def write_all_data(self):
        with open('output_folder/output_data.json', 'w') as f:
            f.write(self.interface_schema.dumps(self.parsed_data, many=True, ensure_ascii=False, indent=4))
        with open('output_folder/logg_data.json', 'w') as f:
            json.dump(self.analyze(), f, ensure_ascii=False, indent=4)


interface_manager = InterfaceManager()
interface_manager.write_all_data()
