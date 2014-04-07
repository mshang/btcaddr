#!/usr/bin/env python
import subprocess
from StringIO import StringIO
import sys
import hashlib


def unpack_der(der):
    """
    References:
    http://www.itu.int/ITU-T/studygroups/com17/languages/X.680-0207.pdf
    http://tools.ietf.org/html/rfc5915
    http://tools.ietf.org/html/rfc5480
    http://www.secg.org/download/aid-780/sec1-v2.pdf
    """
    buf = StringIO(der)
    assert buf.read(1) == '\x30'
    sequence_len = ord(buf.read(1))
    assert buf.len == sequence_len + 2
    assert buf.read(4) == '\x02\x01\x01\x04'
    private_key_len = ord(buf.read(1))
    assert private_key_len <= 32
    assert private_key_len > 28
    private_key_no_pad = buf.read(private_key_len)
    private_key = ('\x00' * (32 - private_key_len)) + private_key_no_pad
    assert private_key.endswith(private_key_no_pad)
    assert len(private_key) == 32
    assert buf.read(10) == '\xa0\x07\x06\x05\x2b\x81\x04\x00\x0a\xa1'
    public_key_outside_len = ord(buf.read(1))
    public_key_outside = buf.read(public_key_outside_len)
    assert buf.read() == ''
    del buf
    public_key_outside = StringIO(public_key_outside)
    assert public_key_outside.read(1) == '\x03'
    public_key_inside_len = ord(public_key_outside.read(1))
    public_key_inside = public_key_outside.read(public_key_inside_len)
    assert public_key_outside.read() == ''
    del public_key_outside
    assert public_key_inside[0] == '\x00'
    public_key = public_key_inside[1:]
    assert len(public_key) == 65
    assert public_key[0] == '\x04'
    return private_key, public_key


BASE_58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def base58check(app_byte, in_bytes):
    """
    https://en.bitcoin.it/wiki/Base58Check_encoding
    """
    a = app_byte + in_bytes
    b = hashlib.sha256(a).digest()
    assert len(b) == 32
    c = hashlib.sha256(b).digest()
    assert len(c) == 32
    checksum = c[:4]
    d = a + checksum
    e = int(d.encode('hex'), 16)
    reversed_b58 = ''
    while e > 0:
        rem = e % 58
        e /= 58
        reversed_b58 += BASE_58_ALPHABET[rem]
    assert not reversed_b58.endswith('1')
    reversed_b58 += '1' * (len(d) - len(d.lstrip('\x00')))
    return reversed_b58[::-1]


def get_address(public_key):
    """
    https://en.bitcoin.it/wiki/Technical_background_of_Bitcoin_addresses
    """
    a = hashlib.sha256(public_key).digest()
    assert len(a) == 32
    b = hashlib.new('ripemd160')
    b.update(a)
    c = b.digest()
    assert len(c) == 20
    return base58check('\x00', c)


def get_private_key_wif(private_key):
    """
    https://en.bitcoin.it/wiki/Wallet_import_format
    """
    return base58check('\x80', private_key)


if __name__ == '__main__':
    output = subprocess.check_output([
        'openssl', 'ecparam',
        '-param_enc', 'named_curve',
        '-name', 'secp256k1',
        '-genkey',
        '-noout',
        '-outform', 'DER',
        '-conv_form', 'uncompressed',
    ])

    try:
        private_key, public_key = unpack_der(output)
        wif = get_private_key_wif(private_key)
        assert all([c in BASE_58_ALPHABET for c in wif])
        assert wif.startswith('5')
        address = get_address(public_key)
        assert all([c in BASE_58_ALPHABET for c in address])
        assert address.startswith('1')
        print "wif: " + wif
        print "address: " + address
    except Exception:
        print >> sys.stderr, "error for DER: %s" % output.encode('hex')
        sys.exit(1)
