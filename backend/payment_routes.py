import razorpay
import os
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET")

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "supersecretkey"  # change for production
ALGORITHM = "HS256"

wallet_balances = {}

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Invalid token payload")
        return username
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid token")

@router.post("/create-payment")
async def create_payment(request: Request, username: str = Depends(get_current_user)):
    data = await request.json()
    amount_raw = data.get("amount")
    if not amount_raw:
        return JSONResponse({"error": "Missing amount"}, status_code=400)

    amount = int(float(amount_raw) * 100)
    if amount <= 0:
        return JSONResponse({"error": "Amount must be greater than zero"}, status_code=400)

    payment_order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1,
        "notes": {"user_id": username}
    })

    return JSONResponse({
        "order_id": payment_order["id"],
        "razorpay_key": RAZORPAY_KEY_ID,
        "amount": amount
    })

@router.post("/add-funds")
async def add_funds(request: Request, username: str = Depends(get_current_user)):
    data = await request.json()
    amount_raw = data.get("amount")

    if not amount_raw:
        return JSONResponse({"error": "Missing amount"}, status_code=400)

    amount = float(amount_raw)

    current_balance = wallet_balances.get(username, 0)
    wallet_balances[username] = current_balance + amount

    return JSONResponse({"message": f"₹{amount} added to wallet successfully", "balance": wallet_balances[username]})

@router.get("/me")
async def get_me(username: str = Depends(get_current_user)):
    balance = wallet_balances.get(username, 0)
    return {"username": username, "balance": balance}
