#!/usr/bin/env python

import json
from os import listdir
from os.path import (
    join,
    isfile
)
from typing import Dict, List
from eth_account import Account
from hummingbot.cli.settings import get_key_file_path, KEYFILE_PREFIX, KEYFILE_POSTFIX


def create_and_save_wallet(password: str, extra_entropy: str = "") -> Account:
    """
    :param password: client password
    :param extra_entropy: (Optional) adds more randomness to the private key generation process.
    """
    acct: Account = Account.create(extra_entropy)
    return save_wallet(acct, password)


def import_and_save_wallet(password: str, private_key: str) -> Account:
    acct: Account = Account.privateKeyToAccount(private_key)
    return save_wallet(acct, password)


def save_wallet(acct: Account, password: str) -> Account:
    encrypted: Dict = Account.encrypt(acct.privateKey, password)
    file_path: str = "%s%s%s%s" % (get_key_file_path(), KEYFILE_PREFIX, acct.address, KEYFILE_POSTFIX)
    with open(file_path, 'w+') as f:
        f.write(json.dumps(encrypted))
    return acct


def unlock_wallet(public_key: str, password: str) -> Account:
    file_path: str = "%s%s%s%s" % (get_key_file_path(), KEYFILE_PREFIX, public_key, KEYFILE_POSTFIX)
    with open(file_path, 'r') as f:
        encrypted = f.read()
    private_key: str = Account.decrypt(encrypted, password)
    acct: Account = Account.privateKeyToAccount(private_key)
    return acct


def list_wallets() -> List[str]:
    wallets = []
    for f in listdir(get_key_file_path()):
        if isfile(join(get_key_file_path(), f)) and f.startswith(KEYFILE_PREFIX) and f.endswith(KEYFILE_POSTFIX):
            wallets.append(f[len(KEYFILE_PREFIX):-len(KEYFILE_POSTFIX)])
    return wallets

