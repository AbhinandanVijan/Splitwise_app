Splitwise_app
An open-source full-stack web application inspired by Splitwise to manage shared expenses among individuals and groups. This project simplifies the process of tracking, splitting, and settling costs.

Features

🔹 Group Expense Tracking: Log shared expenses and automatically calculate who owes whom.

🔹 User Management: Secure authentication and user sessions.

🔹 Dynamic Settlements: Real-time computation of balances and settlement suggestions.

🔹 Responsive UI: Built for an intuitive and interactive experience across devices.

Technologies Used
Backend:
Python 3.11

FastAPI – for high-performance async REST APIs

SQLAlchemy ORM – for database modeling and interactions

Pydantic – for data validation

JWT (PyJWT) – for secure user authentication

Uvicorn – ASGI server for running FastAPI

Frontend:
React.js – for building the user interface

Tailwind CSS – for utility-first styling

Axios – for making HTTP requests

Database:
SQLite (dev) / Compatible with PostgreSQL, MySQL

NPM – JavaScript package management

Pip – Python dependency management

Getting Started
Prerequisites
Python 3.10+

Node.js & npm

Git

Installation

Clone the Repository

git clone https://github.com/AbhinandanVijan/Splitwise_app.git
cd Splitwise_app


Set Up Backend

cd splitwise_app
pip install -r requirements.txt
uvicorn app:app --reload


Set Up Frontend

cd ../splitwise_frontend/splitwise-frontend
npm install
npm start
Access the App

Visit http://localhost:3000 to start using the Splitwise clone.


