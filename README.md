btcaddr
=======

Generate bitcoin addresses.

Installing
----------

    $ pip install btcaddr

Usage
-----

    $ btcaddr
    wif: 5JJmg63yH9r21XKZfYwp37rFiazH2kX1jdyvzF63FCKfam8NxHn
    address: 1P3hSHjtmekV7M76SbK7EvskwJZ1BeNuoM

Testing
-------

You will need a running bitcoind instance.

1. Generate 1000 addresses.

        $ seq 1 1000 | xargs -n1 btcaddr > btcaddr.out

2. Import the the private keys into bitcoind.

        $ grep 'wif: ' btcaddr.out | cut -d ' ' -f 2 | sort > wif.out
        $ xargs -n1 -I{} -P16 bitcoin-cli importprivkey {} '' false < wif.out

3. Get the private key associated with each address according to bitcoind.

        $ grep 'address: ' btcaddr.out | cut -d ' ' -f 2 | xargs -n1 -I{} -P16 bitcoin-cli dumpprivkey {} | sort > dumpprivkey.out

4. Compare with the generated private keys.

        $ diff dumpprivkey.out wif.out
