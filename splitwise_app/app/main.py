from fastapi import FastAPI
from app.db.init_db import init_db
from app.api.v1.routes import user
from app.api.v1.routes import group
from app.api.v1.routes import expense
from app.api.v1.routes  import settlement
from app.api.v1.routes import summary
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Splitwise App API",
    version="1.0.0",
    description="A backend API for managing groups, expenses, and balances."
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 👈 React Vite server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
init_db()

# Root route for testing
@app.get("/")
def read_root():
    return {"message": "Welcome to the Splitwise App API!"}

app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])

app.include_router(group.router, prefix="/api/v1/groups", tags=["Groups"])

app.include_router(expense.router, prefix="/api/v1/expenses", tags=["Expenses"])

app.include_router(settlement.router, prefix="/api/v1/settlement", tags=["Settlement"])

app.include_router(summary.router, prefix="/api/v1", tags=["Summary"])






