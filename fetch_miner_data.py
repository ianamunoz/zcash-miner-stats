from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import csv
try:
    import progressbar
except:
    progressbar = None
    print('Install the progressbar2 module to show a progress bar')

USERNAME = 'user'
PASSWORD = 'password'
FILENAME = 'zcash-miner-data.csv'

FR_ADDRS = [
    "t3Vz22vK5z2LcKEdg16Yv4FFneEL1zg9ojd",
    "t3cL9AucCajm3HXDhb5jBnJK2vapVoXsop3",
    "t3fqvkzrrNaMcamkQMwAyHRjfDdM2xQvDTR",
    "t3TgZ9ZT2CTSK44AnUPi6qeNaHa2eC7pUyF",
    "t3SpkcPQPfuRYHsP5vz3Pv86PgKo5m9KVmx",
    "t3Xt4oQMRPagwbpQqkgAViQgtST4VoSWR6S",
    "t3ayBkZ4w6kKXynwoHZFUSSgXRKtogTXNgb",
    "t3adJBQuaa21u7NxbR8YMzp3km3TbSZ4MGB",
    "t3K4aLYagSSBySdrfAGGeUd5H9z5Qvz88t2",
    "t3RYnsc5nhEvKiva3ZPhfRSk7eyh1CrA6Rk",
    "t3Ut4KUq2ZSMTPNE67pBU5LqYCi2q36KpXQ",
    "t3ZnCNAvgu6CSyHm1vWtrx3aiN98dSAGpnD",
    "t3fB9cB3eSYim64BS9xfwAHQUKLgQQroBDG",
    "t3cwZfKNNj2vXMAHBQeewm6pXhKFdhk18kD",
    "t3YcoujXfspWy7rbNUsGKxFEWZqNstGpeG4",
    "t3bLvCLigc6rbNrUTS5NwkgyVrZcZumTRa4",
    "t3VvHWa7r3oy67YtU4LZKGCWa2J6eGHvShi",
    "t3eF9X6X2dSo7MCvTjfZEzwWrVzquxRLNeY",
    "t3esCNwwmcyc8i9qQfyTbYhTqmYXZ9AwK3X",
    "t3M4jN7hYE2e27yLsuQPPjuVek81WV3VbBj",
    "t3gGWxdC67CYNoBbPjNvrrWLAWxPqZLxrVY",
    "t3LTWeoxeWPbmdkUD3NWBquk4WkazhFBmvU",
    "t3P5KKX97gXYFSaSjJPiruQEX84yF5z3Tjq",
    "t3f3T3nCWsEpzmD35VK62JgQfFig74dV8C9",
    "t3Rqonuzz7afkF7156ZA4vi4iimRSEn41hj",
    "t3fJZ5jYsyxDtvNrWBeoMbvJaQCj4JJgbgX",
    "t3Pnbg7XjP7FGPBUuz75H65aczphHgkpoJW",
    "t3WeKQDxCijL5X7rwFem1MTL9ZwVJkUFhpF",
    "t3Y9FNi26J7UtAUC4moaETLbMo8KS1Be6ME",
    "t3aNRLLsL2y8xcjPheZZwFy3Pcv7CsTwBec",
    "t3gQDEavk5VzAAHK8TrQu2BWDLxEiF1unBm",
    "t3Rbykhx1TUFrgXrmBYrAJe2STxRKFL7G9r",
    "t3aaW4aTdP7a8d1VTE1Bod2yhbeggHgMajR",
    "t3YEiAa6uEjXwFL2v5ztU1fn3yKgzMQqNyo",
    "t3g1yUUwt2PbmDvMDevTCPWUcbDatL2iQGP",
    "t3dPWnep6YqGPuY1CecgbeZrY9iUwH8Yd4z",
    "t3QRZXHDPh2hwU46iQs2776kRuuWfwFp4dV",
    "t3enhACRxi1ZD7e8ePomVGKn7wp7N9fFJ3r",
    "t3PkLgT71TnF112nSwBToXsD77yNbx2gJJY",
    "t3LQtHUDoe7ZhhvddRv4vnaoNAhCr2f4oFN",
    "t3fNcdBUbycvbCtsD2n9q3LuxG7jVPvFB8L",
    "t3dKojUU2EMjs28nHV84TvkVEUDu1M1FaEx",
    "t3aKH6NiWN1ofGd8c19rZiqgYpkJ3n679ME",
    "t3MEXDF9Wsi63KwpPuQdD6by32Mw2bNTbEa",
    "t3WDhPfik343yNmPTqtkZAoQZeqA83K7Y3f",
    "t3PSn5TbMMAEw7Eu36DYctFezRzpX1hzf3M",
    "t3R3Y5vnBLrEn8L6wFjPjBLnxSUQsKnmFpv",
    "t3Pcm737EsVkGTbhsu2NekKtJeG92mvYyoN",
]

# Block height 1 (genesis block coinbase details can't be accessed)
cur_block_hash = '0007bc227e1c57a4a70e237cad00e7b7ce565155ab49166bc57397a26d339283'

rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8232" % (USERNAME, PASSWORD))

# Work out where we should start
try:
    with open(FILENAME, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        row = None
        for row in reader:
            pass
        if row:
            # row is now on the last line
            cur_block_hash = rpc_connection.getblock(row[0]).get('nextblockhash', None)
except FileNotFoundError:
    pass

cur_height = rpc_connection.getblockcount()
pbar = progressbar.ProgressBar(max_value=cur_height) if progressbar else None

with open(FILENAME, 'a') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    while cur_block_hash:
        block_data = rpc_connection.getblock(cur_block_hash)
        cb_data = rpc_connection.getrawtransaction(block_data['tx'][0], 1)

        miner = ('', 0)
        fr = []
        others = []
        for vout in cb_data['vout']:
            addr = '#'.join(vout['scriptPubKey']['addresses'])
            value = vout['value']
            if addr in FR_ADDRS:
                fr.append(value)
                continue
            if value > miner[1]:
                if miner[0]:
                    others.append(miner)
                miner = (addr, value)
            else:
                others.append((addr, value))

        height = block_data['height']
        # Average over 100 blocks, to make the data more versatile
        netsolps = rpc_connection.getnetworksolps(100, height)
        writer.writerow([
            height,
            block_data['time'],
            netsolps,
            '%s~%s' % miner,
            '/'.join(['%s' % v for v in fr]),
            '/'.join(['%s~%s' % other for other in others]),
        ])

        if pbar and height <= cur_height:
            pbar.update(height)
        cur_block_hash = block_data.get('nextblockhash', None)
