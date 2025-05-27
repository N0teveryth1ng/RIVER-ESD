# pricing engine -- >

def calculate_price(demand, seller_supply, price_per_kwh):
      
      if demand <= seller_supply:
         unit_sold = demand
         total_price = unit_sold * price_per_kwh
         print(f"Order Matched: {unit_sold} kwh sold for {total_price}")
         return {
              'unit_sold': unit_sold,
              'total_price': total_price
         }
      
      else: # partial supply
         unit_sold = seller_supply
         shortage = demand - seller_supply
         total_price = unit_sold * price_per_kwh
         print(f"Partially matched: {unit_sold} kWh sold for ₹{total_price},")
         print(f"Remaining {shortage} kWh to be handled by GRID or next sellers.")
         return {
              'unit_sold': unit_sold,
              'total_price': total_price
         }
      
