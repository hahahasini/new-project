# Functional Requirements

> **Project**: PLACEHOLDER-PROJECT-NAME — Vitamin Deficiency Detection System  
> **Version**: 1.0.0 | **Last Updated**: PLACEHOLDER-YEAR

---

## Overview

This document specifies all functional requirements for the PLACEHOLDER-PROJECT-NAME system, organized by module. Each requirement follows the format `FR<Module>.<Sequence>` and includes a detailed description, acceptance criteria, and dependency information. The system comprises four core modules: Image Analysis Engine, Diet Recommendation Engine, Nearby Doctors Locator, and User Interface.

---

## Module 1: Image Analysis Engine

### FR1.1: Body Part Selection
**Description**: The system shall provide users with a mechanism to select the body part category (Nail, Tongue, or Skin) before submitting an image for analysis. The selection determines which specialized CNN model processes the uploaded image.  
**Acceptance Criteria**:
- Three distinct body part options are presented: Nail, Tongue, Skin
- Each option navigates to a dedicated analysis page (`/nail`, `/tongue`, `/skin`)
- Body part selection is passed to the backend as a `body_part` form field
- Invalid body part values trigger a 400 HTTP error with descriptive message
- Each analysis page displays the specific deficiencies it detects (e.g., "Detects Iodine & Vitamin D Deficiencies" for Nail)  
**Dependencies**: None (entry-level requirement)

### FR1.2: Image Upload via Drag-and-Drop
**Description**: The system shall accept image uploads through a drag-and-drop interface that supports both file dragging from the operating system's file manager and clicking to open a file browser dialog. The dropzone shall provide visual feedback during drag operations.  
**Acceptance Criteria**:
- Dropzone area accepts `dragover`, `dragleave`, and `drop` events
- Visual state changes when a file is dragged over the dropzone (highlighted border/background)
- Clicking the dropzone opens a file input dialog filtered to `image/jpeg,image/png,image/jpg`
- Only files with MIME type starting with `image/` are accepted via drag-and-drop
- A hidden `<input type="file">` element handles the underlying file selection
- Keyboard accessibility: pressing Enter on the focused dropzone triggers file selection  
**Dependencies**: FR1.1

### FR1.3: Image Preview
**Description**: Upon selecting an image file, the system shall display a preview of the selected image within the upload area, replacing the dropzone UI. The preview uses a browser-generated object URL (`URL.createObjectURL`) for zero-latency rendering without server upload.  
**Acceptance Criteria**:
- Preview image renders immediately after file selection (no upload required)
- The preview replaces the dropzone area
- Image displays with appropriate CSS styling to maintain aspect ratio
- Previous results and errors are cleared when a new image is selected
- Object URLs are properly managed to prevent memory leaks  
**Dependencies**: FR1.2

### FR1.4: Image Analysis Execution
**Description**: The system shall transmit the selected image and body part to the backend API for analysis when the user triggers the "Analyze Image" action. The frontend sends a `multipart/form-data` POST request to `/api/analyze` containing the image file and body part string.  
**Acceptance Criteria**:
- The "Analyze Image" button is enabled only when an image is selected and the body part is valid
- A loading spinner and "Analyzing..." text replace the button label during processing
- The button is disabled during analysis to prevent duplicate submissions
- The HTTP request uses `multipart/form-data` content type
- The request timeout is set to 60 seconds to accommodate model inference time
- Network errors produce a specific message: "Cannot connect to the server. Please ensure the backend is running on port 8000."
- Server-side validation errors display the `detail` field from the HTTP error response
- Generic failures display: "Analysis failed. Please try again with a different image."  
**Dependencies**: FR1.2, FR1.3

### FR1.5: Server-Side Image Validation
**Description**: The backend shall validate uploaded images before processing, rejecting invalid files with appropriate HTTP error responses.  
**Acceptance Criteria**:
- Only JPEG and PNG MIME types are accepted (`image/jpeg`, `image/png`, `image/jpg`)
- Non-image files return HTTP 400 with message: "Only JPEG and PNG images are supported."
- Corrupted or unreadable images return HTTP 400 with message: "Invalid image file: {error detail}"
- Body part validation rejects values not in `["Nail", "Skin", "Tongue"]` with HTTP 400
- All validation occurs before model inference to avoid wasted compute  
**Dependencies**: FR1.4

### FR1.6: CNN Model Inference
**Description**: The system shall preprocess the validated image and execute inference using the body-part-specific TensorFlow/Keras CNN model. Preprocessing consists of: (1) decoding raw bytes to NumPy array via OpenCV, (2) converting BGR to RGB color space, (3) resizing to 224×224 pixels, (4) normalizing pixel values to [0, 1] float32 range, and (5) expanding dimensions to add a batch axis.  
**Acceptance Criteria**:
- The correct model is selected based on the `body_part` parameter
- Image preprocessing produces a 4D tensor of shape `(1, 224, 224, 3)` with float32 dtype
- Model prediction returns a probability distribution across all classes for the body part
- The class with the highest probability is selected via `numpy.argmax`
- Confidence is calculated as `max(prediction) × 100`, rounded to 2 decimal places
- The predicted class index maps to both a deficiency label (from `CLASSES`) and a disease label (from `DISEASES`)
- If the model file is unavailable, the system generates mock predictions using `numpy.random.dirichlet` and flags `used_model = False`  
**Dependencies**: FR1.5

### FR1.7: Prediction Results Display
**Description**: The system shall display analysis results in a structured `ResultsPanel` component showing the detected body part, disease condition, vitamin deficiency, and confidence score with a color-coded confidence indicator.  
**Acceptance Criteria**:
- Results appear with a fade-in animation after analysis completes
- Four result items display: Body Part, Detected Condition, Vitamin Deficiency, Confidence
- Confidence is color-coded: green (≥80%), amber (≥50%), red (<50%)
- A confidence bar visually represents the confidence percentage
- If mock predictions were used, a prominent warning displays: "Mock Prediction: The model could not be loaded. These results are simulated."
- Skeleton loading placeholders display during analysis (before results arrive)  
**Dependencies**: FR1.6

### FR1.8: Confidence Score Visualization
**Description**: The system shall render a bar chart showing per-class confidence scores for all classes evaluated by the model, enabling users to see the relative probabilities across all possible diagnoses.  
**Acceptance Criteria**:
- A horizontal bar chart renders using Chart.js via `react-chartjs-2`
- All prediction classes are displayed, sorted by confidence (descending)
- Bars use distinct colors for visual differentiation (indigo, cyan, purple, amber, green, red)
- Y-axis shows percentage (0–100%) with tick marks
- Tooltips show exact percentage values on hover (formatted to 1 decimal place)
- Chart is responsive and maintains a 1.8:1 aspect ratio
- Chart styling adapts to the current theme  
**Dependencies**: FR1.7

### FR1.9: Analysis Reset
**Description**: The system shall provide a "Clear" action that resets the analysis page to its initial state, clearing the selected image, preview, results, and any error messages.  
**Acceptance Criteria**:
- Clicking "Clear" removes the image preview and restores the dropzone
- All state variables reset: `selectedImage`, `previewUrl`, `results`, `error`
- The "Clear" button is disabled during active analysis
- The results panel slides out or disappears  
**Dependencies**: FR1.3, FR1.7

---

## Module 2: Diet Recommendation Engine

### FR2.1: Primary Diet Plan Generation
**Description**: Upon completing image analysis, the system shall automatically generate a personalized 7-day weekly diet plan based on the detected vitamin deficiency. The plan provides specific meal recommendations for breakfast, lunch, and dinner for each day of the week.  
**Acceptance Criteria**:
- A diet plan is generated for the top-predicted deficiency
- The plan covers all 7 days (Monday through Sunday)
- Each day includes three meal categories: breakfast, lunch, dinner
- Meals cycle through curated recommendation lists using modular indexing
- The system supports 14 deficiency categories, each with unique food recommendations
- If no recommendation data exists for a deficiency, default placeholder meals display  
**Dependencies**: FR1.6

### FR2.2: Multi-Deficiency Tabbed Diet Plans
**Description**: The system shall generate and display diet plans for all detected deficiencies (not just the top prediction), presented as tabbed panels. Each tab shows the deficiency name and its detection confidence, allowing users to explore dietary recommendations for all potential deficiencies.  
**Acceptance Criteria**:
- Tabs are generated for each deficiency class with confidence ≥ 0.1%
- The "No Vitamin Deficiency" class is excluded from diet plan tabs
- Tabs are sorted by confidence score (descending)
- Each tab displays the deficiency name and confidence percentage
- Clicking a tab switches the visible diet plan with a fade-in animation
- Tab ARIA attributes are properly set (`role="tablist"`, `role="tab"`, `aria-selected`)
- The first (highest confidence) tab is active by default  
**Dependencies**: FR2.1

### FR2.3: Food Recommendations Display
**Description**: Below the weekly meal plan, the system shall display a list of generally recommended foods for the active deficiency as clickable/viewable tags.  
**Acceptance Criteria**:
- Food recommendations appear as styled tag elements (`.food-tag`)
- Recommendations are de-duplicated from the combined breakfast/lunch/dinner pool
- Tags display only when the active plan has food recommendations
- The section heading "🍎 Recommended Foods" is shown above the tags  
**Dependencies**: FR2.1

### FR2.4: Diet Plan Download
**Description**: The system shall provide a "Download All Diet Plans" button that generates a plain-text file containing the weekly diet plans for all detected deficiencies and triggers a browser download.  
**Acceptance Criteria**:
- Clicking "📥 Download All Diet Plans" generates a `.txt` file
- The file includes diet plans for ALL deficiency tabs (not just the active one)
- Each deficiency section includes the name, confidence percentage, and day-by-day meals
- The file is named `diet_plans_all_deficiencies.txt`
- The download uses `Blob` creation and `URL.createObjectURL` for client-side generation
- The temporary object URL is revoked after download to prevent memory leaks  
**Dependencies**: FR2.2

---

## Module 3: Nearby Doctors Locator

### FR3.1: Location Permission Request
**Description**: The system shall request the user's geographic location via the browser's Geolocation API, displaying a clear explanation of why location access is needed and how the data will be used.  
**Acceptance Criteria**:
- A "Find Nearby Doctors" section appears below the diet plan in the results panel
- A call-to-action card explains: "We need your location to find nearby hospitals and doctors. Your location data is only used locally and is never stored."
- The "📍 Share My Location" button triggers `navigator.geolocation.getCurrentPosition`
- High accuracy mode is enabled (`enableHighAccuracy: true`)
- A 10-second timeout prevents indefinite waiting
- A 60-second `maximumAge` allows cached positions
- If location is denied, the error message explains how to re-enable permissions
- If geolocation is unsupported, an appropriate error is displayed
- The button shows "🔄 Retry" after a denial, allowing re-attempts  
**Dependencies**: FR1.7

### FR3.2: Hospital/Clinic Data Retrieval
**Description**: Upon receiving the user's coordinates, the system shall query the Overpass API (OpenStreetMap) to retrieve nearby hospitals, clinics, and medical practices within a configurable radius.  
**Acceptance Criteria**:
- The Overpass query searches for: `amenity=hospital`, `amenity=clinic`, `amenity=doctors`, `healthcare=doctor`, `healthcare=hospital` (both node and way elements)
- Default search radius is 5000 meters
- Results are limited to the top 20 entries (sorted by generated rating)
- Only entries with a `name` tag are included in results
- Each result includes: id, name, latitude, longitude, type, phone, website, address
- Generated pseudo-random ratings (3.2–5.0) and review counts (20–500) are assigned based on the element's OSM ID for consistency
- Results are automatically re-fetched when the search radius changes  
**Dependencies**: FR3.1

### FR3.3: Interactive Map Display
**Description**: The system shall render an interactive map showing the user's location and nearby medical facilities using Leaflet with OpenStreetMap tiles.  
**Acceptance Criteria**:
- Map renders using CartoDB dark tile layer (`dark_all`)
- User location is shown with a pulsing blue dot marker (custom `DivIcon`)
- Hospital/clinic locations are shown with standard Leaflet markers
- Clicking a marker shows a popup with: name, star rating, review count, address, phone
- Map auto-fits bounds to show all markers with 40px padding
- Maximum auto-zoom is capped at level 14 to maintain context
- Map height is 380px with rounded corners (0.75rem border-radius)
- Scroll wheel zoom is enabled for exploration
- A loading overlay with spinner appears during data fetching  
**Dependencies**: FR3.2

### FR3.4: Search Radius Configuration
**Description**: The system shall allow users to adjust the search radius for nearby doctors via a dropdown selector with preset values.  
**Acceptance Criteria**:
- A dropdown labeled "Radius:" offers: 2 km, 5 km, 10 km, 20 km
- Default selection is 5 km
- Changing the radius triggers a new Overpass API query with the updated radius
- The map and list update to reflect the new search area
- A "No hospitals or clinics found within X km" message shows when results are empty  
**Dependencies**: FR3.2, FR3.3

### FR3.5: Doctor List with Distance
**Description**: Below the map, the system shall render a scrollable list of found medical facilities, each displaying the facility name, type badge, rating, address, phone, distance from user, and website link.  
**Acceptance Criteria**:
- Each card shows: type emoji+label (🏥 Hospital, 🩺 Clinic, 👨‍⚕️ Doctor), name, star rating, review count, address (if available), phone (if available)
- Distance is calculated using the Haversine formula and displayed in km (1 decimal)
- Cards are clickable, toggling a selected state (highlighted border)
- Website links open in a new tab (`target="_blank"`, `rel="noopener noreferrer"`)
- Cards use glassmorphism styling (`.glass` class)
- Staggered animation on card appearance  
**Dependencies**: FR3.2

### FR3.6: Deficiency-Contextualized Doctor Search
**Description**: When the detected deficiency is not "No Vitamin Deficiency," the system shall display a contextual hint suggesting the user seek consultation for the specific deficiency.  
**Acceptance Criteria**:
- A hint banner shows: "💊 Showing doctors for **{deficiency}** consultation"
- The hint is hidden when the deficiency is "No Vitamin Deficiency"
- The CTA text adapts: "Get checked for {deficiency} — find hospitals & specialists near you."  
**Dependencies**: FR1.7, FR3.1

---

## Module 4: User Interface & Navigation

### FR4.1: Application Navigation
**Description**: The system shall provide a responsive navigation bar with links to the home page and each analysis page, supporting both desktop and mobile viewports.  
**Acceptance Criteria**:
- Desktop navbar shows: VitaDetect logo/text (home link), Nail Analysis, Tongue Analysis, Skin Analysis links
- Active route is visually highlighted (`.nav-link--active`)
- Navbar gains a frosted-glass background effect when the page is scrolled past 20px
- Mobile: a hamburger menu (☰) toggles a dropdown menu with animated open/close
- The mobile menu closes when a link is clicked
- Theme toggle button (🌙/☀️) is always visible in the navbar controls  
**Dependencies**: None

### FR4.2: Dark/Light Theme Toggle
**Description**: The system shall support two visual themes (light and dark) toggled via a button in the navigation bar, with the selected theme applied globally via CSS custom properties.  
**Acceptance Criteria**:
- Default theme is `light` on every page load (no localStorage persistence across sessions)
- Clicking the theme toggle switches between light (☀️ icon) and dark (🌙 icon) modes
- The theme is applied by setting `data-theme` attribute on `<html>` element
- All CSS color variables respect the `[data-theme="dark"]` selector
- The theme context (`ThemeProvider`) wraps the entire application
- The toggle button includes ARIA label: "Switch to light/dark theme"  
**Dependencies**: None

### FR4.3: Home Page Model Cards
**Description**: The home page shall display three model cards (Nail, Tongue, Skin) with images, descriptions, and call-to-action buttons linking to the respective analysis pages.  
**Acceptance Criteria**:
- Three model cards render in a responsive grid layout
- Each card contains: realistic image, title, subtitle pill (deficiency types), description, "Analyze Now →" CTA button
- Cards use accent color coding: indigo (Nail), rose (Tongue), cyan (Skin)
- Images have gradient overlays matching the card accent color
- Cards include image lazy loading (`loading="lazy"`)
- Cards are wrapped in `<article>` elements with ARIA labels  
**Dependencies**: FR4.1

### FR4.4: How It Works Section
**Description**: The home page shall include a step-by-step "How It Works" section explaining the analysis workflow in four steps.  
**Acceptance Criteria**:
- Four step cards display: (01) Upload a Photo, (02) Model Analysis, (03) Review Your Results, (04) Next Steps
- Each step includes a numbered badge, title, and description
- Steps use glassmorphism styling
- The section animates on scroll (fade-in-up)  
**Dependencies**: None

### FR4.5: Statistics Display
**Description**: The home page shall display key system statistics in a horizontal row with glassmorphism cards.  
**Acceptance Criteria**:
- Four stats display: "3 Specialized Models", "< 2s Average Analysis Time", "3+ Deficiencies Detected", "100% Private - Runs Locally"
- Stats use the `.glass` class for visual styling
- Staggered entrance animation  
**Dependencies**: None

### FR4.6: Medical Disclaimer
**Description**: The home page shall display a medical disclaimer at the bottom informing users that the tool is not a substitute for professional medical advice.  
**Acceptance Criteria**:
- Disclaimer text: "**Medical Disclaimer:** VitaDetect is designed to provide helpful insights, not medical advice. Always consult a qualified healthcare professional before making any health decisions."
- Disclaimer is visually distinct with bold label
- Displayed on the home page with fade-in animation  
**Dependencies**: None

### FR4.7: Analysis Page Tips
**Description**: Each analysis page shall display contextual tips for achieving optimal analysis results.  
**Acceptance Criteria**:
- Tip card appears below the page header with an info icon
- Nail page tip: "Use a well-lit photo of a bare nail (no polish). Capture one fingernail clearly against a plain background. JPG or PNG, max 10 MB."
- Tips use glassmorphism styling
- Tips animate in with the page load  
**Dependencies**: FR1.1

### FR4.8: API Health Check
**Description**: The system shall expose a health check endpoint allowing monitoring tools and the frontend to verify the backend's operational status.  
**Acceptance Criteria**:
- `GET /api/health` returns a JSON response with: `status`, `models_loaded`, `version`, `available_models`
- `status` is "healthy" when the server is operational
- `models_loaded` is `true` when at least one model was successfully loaded
- `available_models` lists the body parts with loaded models (e.g., `["Nail", "Skin", "Tongue"]`)
- Response conforms to the `HealthCheckResponse` Pydantic schema  
**Dependencies**: None

---

## Requirement Traceability Matrix

| Requirement | Module | Priority | Status |
|:---:|:---|:---:|:---:|
| FR1.1–FR1.9 | Image Analysis Engine | P0 – Critical | ✅ Implemented |
| FR2.1–FR2.4 | Diet Recommendation Engine | P0 – Critical | ✅ Implemented |
| FR3.1–FR3.6 | Nearby Doctors Locator | P1 – Important | ✅ Implemented |
| FR4.1–FR4.8 | User Interface & Navigation | P0 – Critical | ✅ Implemented |

**Total Functional Requirements**: 27  
**Implemented**: 27/27 (100%)

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
