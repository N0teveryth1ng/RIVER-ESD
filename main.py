# simulating orders as tests

from gridSim.order_handler import handle_buy_order

# Sample buyer order
buyer_order = { 'Energy needed': 9999 }

# Sample sellers supply
seller_supply = [
    {'id': 'S1', 'available_energy': 0},
    {'id': 'S2', 'available_energy': 0},
    {'id': 'S3', 'available_energy': 0},
]


result = handle_buy_order(buyer_order, seller_supply)

print('Results: ')
for i in result:
    print(i)






