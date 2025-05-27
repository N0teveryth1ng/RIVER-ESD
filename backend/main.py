from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
from gridSim.wallet import get_balance, update_wallet, deduct_wallet, add_funds
from backend.auth_routes import router as auth_router, verify_user
from backend.payment_routes import router as payment_router
from fastapi import Request



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(payment_router)

# Serve frontend
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

# Security
security = HTTPBasic()

# Protected example endpoint
@app.get("/protected")
async def protected_route(username: str = Depends(verify_user)):
    return {"message": f"Hello {username}, this is protected!"}


# Your existing routes...
@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.post("/make-order")
async def make_order(data: dict, username: str = Depends(verify_user)):
    # Modified to use authenticated user
    buyer_id = username  # Now using logged-in user
    demand = data['demand']
    seller_supply = data['sellers']
    price_per_kwh = 3.5

    total_cost = 0
    result = []
    remaining = demand

    for s in seller_supply:
        if remaining <= 0:
            break

        sold = min(remaining, s['available_energy'])
        cost = sold * price_per_kwh

        if get_balance(buyer_id) < cost:
            raise HTTPException(status_code=400, detail="Insufficient balance")

        deduct_wallet(buyer_id, cost)
        update_wallet(s['id'], cost)

        result.append({
            "seller": s['id'],
            "sold": sold,
            "price": cost
        })

        remaining -= sold
        total_cost += cost

    return {
        "buyer": buyer_id,
        "orders": result,
        "total_spent": total_cost,
        "remaining_demand": remaining,
        "buyer_balance": get_balance(buyer_id)
    }

@app.post("/add-funds")
async def add_funds_api(data: dict, username: str = Depends(verify_user)):

    amount = data.get('amount')
    if not amount:
        raise HTTPException(status_code=400, detail="Amount is required")
    
    new_balance = add_funds(username, amount)
    # Update the simple user DB balance as well
    # users_db[username]["balance"] = new_balance
    
    return {
        "message": f"₹{amount} added",
        "new_balance": new_balance
    }


# get balance --> 
@app.get("/get-balance")
async def get_balance_api(username: str = Depends(auth_router.verify_user)):
    balance = get_balance(username)  # your existing fuction from gridSim.wallet
    return {"balance": balance}







