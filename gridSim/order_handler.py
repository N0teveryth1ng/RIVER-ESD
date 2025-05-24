
# Buy_ order class -->
class BuyOrder:
    def __init__(self, buyer_id, quantity_kwh, max_price_per_kwh):
        self.buyer_id = buyer_id
        self.quantity_kwh = quantity_kwh
        self. max_price_per_kwh =  max_price_per_kwh


# handles buyers orders -->
from gridSim.matching_orders import match_order

# handles multiple aggregates order -- >  
def handle_buy_order(buyer_order, seller_supply):
    demanded = buyer_order['Energy needed']
    matched_seller = [] # energy seller sold will be appended here after the deal for storing

    for seller in seller_supply:
        if demanded <= 0:
            break

        available = seller['available_energy']
        energy_to_take = min(available, demanded)   

        if energy_to_take > 0:
            matched_seller.append({
                'seller_id': seller['id'],
                'energy_sold': energy_to_take
            })
             
        seller['available_energy'] -= energy_to_take # sellers supply left
        demanded -= energy_to_take  # buyer's demand left 

    # GRID enables at shortage -- >
    if demanded > 0:
        matched_seller.append({
            'source': 'GRID' ,
            'energy_sent': demanded
            })    
         
    print('order recived: ✅')
    return matched_seller



 



