# -----------------------------------------------------------------------------
# Copyright (C) 2019 Xinyu Ma
#
# This file is part of python-ndn.
#
# python-ndn is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# python-ndn is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with python-ndn.  If not, see <https://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------
import abc
from typing import Tuple
from Cryptodome.Hash import SHA256
from Cryptodome.Random import get_random_bytes
from ...encoding import Signer, NonStrictName, BinaryStr, FormalName, Component
from ..consts import KEY_COMPONENT


class Tpm(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_signer(self, key_name: NonStrictName) -> Signer:
        pass

    @abc.abstractmethod
    def generate_key(self, id_name: FormalName, key_type: str = 'rsa', **kwargs) -> Tuple[FormalName, BinaryStr]:
        pass

    @abc.abstractmethod
    def has_key(self, key_name: FormalName) -> bool:
        pass

    def construct_key_name(self, id_name: FormalName, pub_key: BinaryStr, **kwargs) -> FormalName:
        key_id = kwargs.pop('key_id', None)
        key_id_type = kwargs.pop('key_id_type', 'random')
        if not key_id:
            if key_id_type == 'random':
                while True:
                    key_id = Component.from_bytes(get_random_bytes(8))
                    if not self.has_key(id_name + [KEY_COMPONENT, key_id]):
                        break
            elif key_id_type == 'sha256':
                h = SHA256.new()
                h.update(pub_key)
                key_id = Component.from_bytes(h.digest())
            else:
                raise ValueError(f'KeyIdType not supported: {key_id_type}')
        return id_name + [KEY_COMPONENT, key_id]
