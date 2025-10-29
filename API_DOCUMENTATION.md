# API Documentation

## Overview
This document provides an overview of the API endpoints available in the Django backend project. Each app's endpoints are listed with their respective base URLs and descriptions.

---

## API Endpoints by App

### **`varchas_iitj` (Main URL Configuration)**
- **Base URL**: `/`
- **Endpoints**:
  - `/webd` - Admin site
  - `/login` - Custom login view
  - `/logout` - Logout view
  - `/admin` - Includes `adminportal.urls`
  - `/` - Includes `main.urls`
  - `/ckeditor` - CKEditor uploader
  - `/account` - Includes `accounts.urls`
  - `/registration` - Includes `registration.urls`
  - `/sponsors` - Includes `sponsors.urls`
  - `/app_apis` - Includes `app_apis.urls`
  - `/referees` - Includes `referees.urls`
  - `/` - Django authentication URLs

---

### **`accounts`**
- **Base URL**: `/account/`
- **Endpoints**:
  - `/` - REST API for users and groups
  - `/api-auth/` - REST framework authentication
  - `/userregister/` - User registration
  - `/google-signup/` - Google signup
  - `/updateInfo/` - Update user information

---

### **`sponsors`**
- **Base URL**: `/sponsors/`
- **Endpoints**:
  - `/sponsorapi/` - Sponsor-related APIs
  - `/api-auth/` - REST framework authentication

---

### **`referees`**
- **Base URL**: `/referees/`
- **Endpoints**:
  - `/referees/` - Handles:
    - **GET**: List all referees
    - **POST**: Create a new referee
  - `/referees/<id>/` - Handles:
    - **GET**: Retrieve a referee by ID
    - **PUT**: Replace a referee
    - **PATCH**: Partially update a referee
    - **DELETE**: Delete a referee

---

### **`registration`**
- **Base URL**: `/registration/`
- **Endpoints**:
  - `/` - REST API for teams
  - `/removeplayer/` - Remove a player
  - `/createteam/` - Create a team
  - `/teams/` - List team registrations

---

### **`main`**
- **Base URL**: `/`
- **Endpoints**:
  - `/payment` - Payment processing
  - `/mainapi/` - Team-related API
  - `/api-auth/` - REST framework authentication
  - `/` - Home page

---

### **`adminportal`**
- **Base URL**: `/admin/`
- **Endpoints**:
  - `/mail` - Send mail
  - `/updateScore/(<str:sport>)/` - Update score for a sport
  - `/teams` - Dashboard for teams
  - `/users` - Dashboard for users
  - `/excel` - Download team information as Excel
  - `/` - Admin dashboard

---

### **`app_apis`**
- **Base URL**: `/app_apis/`
- **Endpoints**:
  - `/get_matches/` - Get matches
  - `/sponsors/` - Get sponsors
  - `/informals/` - Get informal events
  - `/score/` - Get score links

---

## Notes
- All endpoints prefixed with `/api-auth/` are for REST framework authentication.
- The project uses Django REST Framework for API development.
- Some endpoints are dynamically generated using `DefaultRouter` in Django REST Framework.