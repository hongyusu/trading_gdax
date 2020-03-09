import cbpro

passphrase='3rkl1v1s8xxd'
b64secret='3tWVhLZj1NNPE7S42T9w/S2MHPiTcoRuQEyT2mjtVStvl/fAHaBXhy2aM5LGZwRAO3S9eZ+HyGTdpwxXdvP4+dg=='
key='33f03384eef6e18b6848573b61686a745'

auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase)
auth_client = cbpro.AuthenticatedClient(key, b64secret, passphrase,api_url="https://api.pro.coinbase.com")

accounts = auth_client.get_accounts()
for account in accounts:
    print(account)
