import time
import logging
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from utils.security import verify_password, create_access_token, get_db
from utils import operations
import models
from fastapi.security import OAuth2PasswordRequestForm
from routes.user import router as user_router
from routes.wallets import router as wallet_router
from routes.coin import router as coin_router
from schemas import user_schema

# Configure logging (writes errors to app.log)
logging.basicConfig(filename="app.log", level=logging.ERROR)

app = FastAPI(title="Stock Trading Application")

@app.middleware("http")
async def custom_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
    except HTTPException as e:
        logging.error(f"HTTPException: {e.detail}")
        return JSONResponse(
            status_code=e.status_code,
            content={"error": e.detail},
        )
    except Exception as e:
        logging.error(f"Unhandled Exception: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal Server Error", "details": str(e)},
        )
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/signup", response_model=user_schema.UserResponse)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    return operations.create_user(db, user)


app.include_router(user_router)
app.include_router(wallet_router)
app.include_router(coin_router)
