# Use Case Specification

> **Project**: PLACEHOLDER-PROJECT-NAME — Vitamin Deficiency Detection System  
> **Version**: 1.0.0 | **Last Updated**: PLACEHOLDER-YEAR

---

## Overview

This document defines all actors, use cases, and system boundaries for PLACEHOLDER-PROJECT-NAME. The system has 21 use cases spanning image analysis, diet recommendation, doctor location, and UI navigation.

See also: [Use Case Diagram](../diagrams/usecase.puml)

---

## 1. Actors

### 1.1 Primary Actors

| Actor | Description | Capabilities |
|:---|:---|:---|
| **End User** | Any individual accessing the web application through a browser | Uploads images, views results, interacts with diet plans and maps, toggles theme, navigates pages |

### 1.2 System Actors

| Actor | Description | Capabilities |
|:---|:---|:---|
| **System (Automated)** | The backend server performing automated processing | Preprocesses images, executes model inference, generates diet plans, calculates distances |

### 1.3 External Actors

| Actor | Description | Capabilities |
|:---|:---|:---|
| **Overpass API** | OpenStreetMap query service providing geospatial data | Returns hospital/clinic data within a geographic radius |
| **Browser Geolocation** | Browser API providing GPS coordinates | Returns latitude/longitude of user's device |

---

## 2. Use Case Descriptions

### UC1: Select Body Part
- **Actor**: End User
- **Description**: User selects which body part to analyze (Nail, Tongue, or Skin) by navigating to the respective analysis page
- **Precondition**: User is on the home page
- **Main Flow**: (1) User views model cards; (2) User clicks "Analyze Now →" on desired card; (3) System navigates to `/nail`, `/tongue`, or `/skin`
- **Postcondition**: Analysis page for selected body part is displayed
- **Alternative Flow**: User can also navigate via the navbar links

### UC2: Upload Image
- **Actor**: End User
- **Description**: User provides an image file through drag-and-drop or file browser dialog
- **Precondition**: User is on an analysis page
- **Main Flow**: (1) User drags image over dropzone OR clicks dropzone; (2) System validates file type; (3) System generates preview URL
- **Postcondition**: Image is loaded in client memory with preview displayed
- **Alternative Flow**: If file is not an image, it is silently rejected

### UC3: Preview Image
- **Actor**: End User
- **Included by**: UC2
- **Description**: System displays a preview of the selected image
- **Precondition**: Image file selected via UC2
- **Main Flow**: Preview renders via `URL.createObjectURL`; dropzone is replaced by image
- **Postcondition**: User can see the selected image before analysis

### UC4: Analyze Image
- **Actor**: End User
- **Description**: User triggers the analysis pipeline by clicking "Analyze Image"
- **Precondition**: Image is selected (UC2), body part is valid (UC1)
- **Main Flow**: (1) Frontend sends POST /api/analyze; (2) Backend validates, preprocesses, runs inference; (3) Backend generates diet plans; (4) Response returned to frontend
- **Includes**: UC18 (Preprocess Image), UC19 (Run CNN Inference), UC20 (Generate Diet Plan)
- **Postcondition**: Analysis results displayed in ResultsPanel
- **Exception Flow**: Network error → error message; Invalid image → 400 error displayed

### UC5: View Results
- **Actor**: End User
- **Description**: User reviews the analysis output showing detected condition, deficiency, and confidence
- **Precondition**: UC4 completed successfully
- **Includes**: UC6 (View Confidence Chart), UC7 (View Diet Plans)
- **Main Flow**: ResultsPanel renders with body part, disease, deficiency, confidence bar
- **Postcondition**: User understands the analysis findings

### UC6: View Confidence Chart
- **Actor**: End User
- **Description**: User views a bar chart showing confidence scores for all prediction classes
- **Precondition**: UC5 results contain prediction_scores
- **Main Flow**: Chart.js bar chart renders with sorted confidence percentages
- **Postcondition**: User understands relative probabilities

### UC7: View Diet Plans
- **Actor**: End User
- **Description**: User views weekly meal plans tailored to detected deficiencies
- **Precondition**: UC5 results contain diet plan data
- **Main Flow**: DietPlan component renders with tabbed interface showing 7-day plans
- **Postcondition**: User has actionable dietary guidance

### UC8: Switch Diet Plan Tabs
- **Actor**: End User
- **Description**: User switches between diet plans for different detected deficiencies
- **Precondition**: Multiple deficiency tabs are available (UC7)
- **Main Flow**: User clicks a tab; active plan changes with fade animation
- **Postcondition**: Selected deficiency's diet plan is displayed

### UC9: Download Diet Plans
- **Actor**: End User
- **Description**: User downloads a text file containing all diet plans
- **Precondition**: Diet plans are displayed (UC7)
- **Main Flow**: Click "Download All" → text file generated → browser download triggered
- **Postcondition**: File `diet_plans_all_deficiencies.txt` saved to user's device

### UC10: Enable Location
- **Actor**: End User, Browser Geolocation
- **Description**: User grants browser location access for nearby doctors search
- **Precondition**: Results displayed with detected deficiency
- **Main Flow**: (1) Click "Share My Location"; (2) Browser prompts for permission; (3) Coordinates received
- **Postcondition**: User coordinates stored in component state
- **Exception Flow**: Permission denied → error message with retry button

### UC11: View Nearby Doctors Map
- **Actor**: End User, Overpass API
- **Description**: User views an interactive map showing nearby hospitals and clinics
- **Precondition**: Location granted (UC10)
- **Includes**: UC21 (Calculate Distances)
- **Main Flow**: (1) Overpass API queried; (2) Map renders with markers; (3) Doctor list displays below
- **Postcondition**: User can see and interact with nearby medical facilities

### UC12: Adjust Search Radius
- **Actor**: End User
- **Description**: User changes the search radius for nearby doctors
- **Precondition**: Map displayed (UC11)
- **Main Flow**: User selects new radius from dropdown (2/5/10/20 km); new query executes
- **Postcondition**: Map and list update with results for new radius

### UC13: View Doctor Details
- **Actor**: End User
- **Description**: User clicks a doctor card or marker to see detailed information
- **Precondition**: Doctor list/map displayed (UC11)
- **Main Flow**: Click card → highlight selection; click marker → show popup with details
- **Postcondition**: Doctor details (name, rating, address, phone, distance) visible

### UC14: Toggle Dark/Light Theme
- **Actor**: End User
- **Description**: User switches between dark and light visual themes
- **Precondition**: Application loaded
- **Main Flow**: Click theme toggle in navbar; `data-theme` attribute updated on `<html>`
- **Postcondition**: All CSS variables update to reflect selected theme

### UC15: Navigate Between Pages
- **Actor**: End User
- **Description**: User navigates between home and analysis pages
- **Precondition**: Application loaded
- **Main Flow**: Click navbar links, model card CTAs, or back buttons
- **Postcondition**: Target page renders without full page reload

### UC16: Reset Analysis
- **Actor**: End User
- **Description**: User clears the current analysis state to start over
- **Precondition**: Image selected or results displayed
- **Main Flow**: Click "Clear" button; all state resets to initial values
- **Postcondition**: Dropzone restored, results cleared

### UC17: Check API Health
- **Actor**: System (Automated)
- **Description**: Monitoring tools query the backend health status
- **Main Flow**: GET /api/health → returns status, model loading state, version, available models
- **Postcondition**: Health information available for monitoring

### UC18: Preprocess Image (System)
- **Actor**: System
- **Included by**: UC4
- **Description**: Backend preprocesses uploaded image for model consumption
- **Main Flow**: Decode bytes → BGR to RGB → resize 224×224 → normalize → batch expand
- **Postcondition**: 4D tensor (1, 224, 224, 3) float32 ready for inference

### UC19: Run CNN Inference (System)
- **Actor**: System
- **Included by**: UC4
- **Description**: Backend executes model prediction on preprocessed image
- **Main Flow**: Select body-part model → model.predict() → argmax → map to labels
- **Postcondition**: Prediction result with deficiency, disease, confidence, scores

### UC20: Generate Diet Plan (System)
- **Actor**: System
- **Included by**: UC4
- **Description**: Backend generates weekly meal plans for detected deficiencies
- **Main Flow**: Lookup food recommendations → cyclic meal assignment → flatten recommendations
- **Postcondition**: 7-day meal plan with food recommendations for each deficiency

### UC21: Calculate Distances (System)
- **Actor**: System
- **Included by**: UC11
- **Description**: Frontend calculates distance between user and each doctor using Haversine formula
- **Main Flow**: For each doctor, compute great-circle distance in km
- **Postcondition**: Distance value displayed on each doctor card

---

## 3. System Boundary

The system boundary encompasses:
- **Inside**: React SPA, FastAPI backend, ML models, image processing, diet generation
- **Outside**: Overpass API, CartoDB tiles, browser geolocation, user's device hardware

The system does **not** include: user authentication, data persistence, payment processing, or real-time camera feed analysis.

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
