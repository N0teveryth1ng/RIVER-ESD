# WALLET FOR USERS -- >

# gridSim/wallet.py

wallets = {
    'user_001': 10000,
    'S1': 0,
    'S2': 0,
    'S3': 0
}
    
def get_balance(user_id):
    return wallets.get(user_id, 0)

def update_wallet(user_id, amount):
    wallets[user_id] = wallets.get(user_id, 0) + amount

def deduct_wallet(user_id, amount):
    if wallets.get(user_id, 0) >= amount:
        wallets[user_id] -= amount
        return True
    return False

def add_funds(user_id, amount):
    update_wallet(user_id, amount)
    return get_balance(user_id)
