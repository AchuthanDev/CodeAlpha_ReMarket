# CodeAlpha_ReMarket
ReMarket: A Second-Hand E-Commerce Marketplace
ReMarket is a full-stack e-commerce web application built with Django. It provides a complete marketplace platform for users to securely buy and sell second-hand products.

🚀 Core Features
Firebase Authentication: Secure user sign-up and login with Google or Email/Password.

Seller Dashboard: Users can easily create, edit, and delete their own product listings.

Product Browsing: A homepage that displays all available items.

Search & Filter: A live search bar for all products and a dynamic category filter.

Shopping Cart: A fully functional cart (add, remove, view items).

Full Checkout: A complete order processing flow that marks items as "sold."

User Profiles: "My Account," "My Listings," and "My Orders" pages for easy management.

Responsive Design: Fully mobile-responsive for all devices, from phones to desktops.



Here is a complete, professional README.md file for your GitHub project.

Just copy and paste the text below into a new file named README.md in your project's main folder (the one with manage.py).

ReMarket: A Second-Hand E-Commerce Marketplace
ReMarket is a full-stack e-commerce web application built with Django. It provides a complete marketplace platform for users to securely buy and sell second-hand products.

Live Demo: [Link to your deployed site on PythonAnywhere or Render]

(Note: Take a screenshot of your homepage and upload it to your GitHub repo, then replace the link below) ``

🚀 Core Features
Firebase Authentication: Secure user sign-up and login with Google or Email/Password.

Seller Dashboard: Users can easily create, edit, and delete their own product listings.

Product Browsing: A homepage that displays all available items.

Search & Filter: A live search bar for all products and a dynamic category filter.

Shopping Cart: A fully functional cart (add, remove, view items).

Full Checkout: A complete order processing flow that marks items as "sold."

User Profiles: "My Account," "My Listings," and "My Orders" pages for easy management.

Responsive Design: Fully mobile-responsive for all devices, from phones to desktops.

🛠️ Implementation & Tech Stack
This project was built using a modern, scalable tech stack.

Backend
Framework: Django (Python)

Database: PostgreSQL (for production) / SQLite3 (for development)

Authentication: Firebase Admin SDK (for verifying user tokens on the backend)

Production Server: Gunicorn

Frontend
Templating: Django Template Language (DTL)

Styling: Custom CSS3 (using Flexbox and Grid)

JavaScript: Vanilla JavaScript for animations and client-side logic

Authentication: Firebase SDK (handles Google/Email login on the client)

Icons: Font Awesome

Deployment
Version Control: Git & GitHub

Hosting: PythonAnywhere / Render

Static Files: WhiteNoise


🏁 How to Run Locally
To get a local copy up and running, follow these steps.

Prerequisites
Python 3.10+

Git

A Firebase project with Authentication (Email/Password & Google) enabled.

Installation
Clone the repository:

Bash

git clone https://github.com/AchuthanDev/CodeAlpha_ReMarket.git
cd CodeAlpha_ReMarket
Create and activate a virtual environment:

Bash

# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
Install dependencies:

Bash

pip install -r requirements.txt
Set up your Firebase Admin Key:

Download your serviceAccountKey.json from your Firebase project settings.

Place it in the root of the project (at the same level as manage.py).

(Note: This file is included in .gitignore and will not be pushed to GitHub).

Run database migrations:

Bash

python manage.py migrate
Run the development server:

Bash

python manage.py runserver
Open http://127.0.0.1:8000/ in your browser.
