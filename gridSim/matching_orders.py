#  test sellers queue -->
sellers = [("seller1", 1000), ("seller2",4000), ("seller2", 6000)]


# macthing order --> [FIFO METHOD]
def match_order(buyer_id, energy_needed):
    
   total_supplied = 0
   fulfilled_by = []  # Seller Details 


   while sellers and total_supplied < energy_needed:
      seller_id, available_energy = sellers.pop(0)


   if available_energy + total_supplied < energy_needed:
      available_energy += total_supplied
      fulfilled_by.append(seller_id, available_energy)
   else: 
       portion = energy_needed - total_supplied
       total_supplied += portion
       fulfilled_by.append((seller_id, portion))

       # reamining energy goes back to seller 
       sellers.insert(0,(seller_id, available_energy - portion))


   for sid, amount in fulfilled_by:
    print(f"sid - {sid}:{amount} kwh")

    print(f"Total supplied: {total_supplied} kwh")   

 


