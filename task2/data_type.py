from dataclasses import dataclass, field
from typing import List

import marshmallow as mm
from dataclasses_json import DataClassJsonMixin, config
from marshmallow import fields


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
