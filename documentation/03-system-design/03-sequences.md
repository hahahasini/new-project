# Sequence Diagrams

> **Project**: PLACEHOLDER-PROJECT-NAME — Vitamin Deficiency Detection System  
> **Version**: 1.0.0 | **Last Updated**: PLACEHOLDER-YEAR

---

## Overview

This document describes the three primary sequence diagrams for PLACEHOLDER-PROJECT-NAME, detailing the message flows, component interactions, data transformations, and error handling for each major workflow.

---

## 1. Sequence Diagram 1 — Image Analysis Workflow

**Diagram**: [sequence1.puml](../diagrams/sequence1.puml)

### 1.1 Purpose
Illustrates the complete flow from image upload through CNN inference to results display. This is the core workflow of the entire application.

### 1.2 Participants
| Participant | Role |
|:---|:---|
| User | Initiates image selection and analysis |
| React Frontend (AnalysisPage) | Manages page state and component rendering |
| ImageUploader Component | Handles drag-and-drop and file selection |
| API Service (Axios) | Constructs and sends HTTP requests |
| FastAPI (Analysis Router) | Receives requests, orchestrates processing |
| Image Processing Utils | Decodes and preprocesses images |
| PredictorService | Manages models and executes inference |
| TensorFlow Model | Performs CNN forward pass |
| DietPlannerService | Generates diet recommendations |
| ResultsPanel Component | Renders analysis results |

### 1.3 Flow Description

**Phase 1 — Image Selection**:
1. User navigates to an analysis page (e.g., `/nail`)
2. ImageUploader renders a dropzone with drag-and-drop support
3. User drops an image file (or clicks to browse)
4. Client validates the file MIME type (`image/*`)
5. Preview URL generated via `URL.createObjectURL(file)`
6. AnalysisPage state updates: `selectedImage`, `previewUrl` set; `results`, `error` cleared

**Phase 2 — Analysis Execution**:
1. User clicks "Analyze Image"
2. Loading state activated: spinner shown, buttons disabled, skeleton ResultsPanel rendered
3. Axios creates `FormData` with `file` and `body_part` fields
4. POST request sent to `http://localhost:8000/api/analyze` (60s timeout)
5. Backend validates: body part ∈ `["Nail", "Skin", "Tongue"]`, content type ∈ `["image/jpeg", "image/png"]`
6. Image bytes decoded to NumPy array via `cv2.imdecode`, converted BGR→RGB

**Phase 3 — Model Inference**:
1. Image resized to 224×224, normalized to float32 [0,1], batch dimension added → shape (1, 224, 224, 3)
2. `model.predict(img_array, verbose=0)` executes CNN forward pass
3. Output: probability vector, e.g., `[0.12, 0.05, 0.83]` for 3-class Nail model
4. `argmax` selects highest-probability class → index 2
5. Index mapped to labels: `CLASSES["Nail"][2]` → "Vitamin D Deficiency", `DISEASES["Nail"][2]` → "Alopecia areata"
6. Confidence = 83.0%

**Phase 4 — Diet Plan Generation**:
1. Primary diet plan generated for top deficiency
2. Loop: diet plans generated for ALL deficiency classes (excluding "No Vitamin Deficiency")
3. Each plan contains 7-day weekly meals and flat food recommendations

**Phase 5 — Response & Display**:
1. Backend constructs `AnalysisResponse` (Pydantic validation)
2. HTTP 200 JSON response returned
3. Frontend updates state: `results` set, `loading` cleared
4. ResultsPanel renders: summary → confidence chart → diet plans → nearby doctors CTA

### 1.4 Error Handling
| Error | HTTP Code | Frontend Display |
|:---|:---:|:---|
| Invalid body part | 400 | Server error detail message |
| Invalid file type | 400 | "Only JPEG and PNG images are supported." |
| Image decode failure | 400 | "Invalid image file: {detail}" |
| Network unreachable | N/A | "Cannot connect to the server..." |
| Generic error | 500 | "Analysis failed. Please try again..." |

### 1.5 Timing
| Stage | Duration |
|:---|:---:|
| Image validation | < 5 ms |
| Image preprocessing | < 30 ms |
| Model inference | 92–146 ms |
| Diet generation | < 20 ms |
| Total server time | ~150–300 ms |
| Network round-trip | < 50 ms (localhost) |
| **End-to-end** | **~200–400 ms** |

---

## 2. Sequence Diagram 2 — Diet Plan Generation & Interaction

**Diagram**: [sequence2.puml](../diagrams/sequence2.puml)

### 2.1 Purpose
Details the diet plan rendering flow including tab switching, meal display, and the text file download mechanism.

### 2.2 Flow Description

**Backend Generation (during /api/analyze)**:
1. `DietPlannerService.generate_weekly_plan(deficiency)` called with detected deficiency string
2. Looks up `FOOD_RECOMMENDATIONS[deficiency]` dictionary
3. For each day (i = 0..6), selects meals via cyclic indexing: `foods["breakfast"][i % len]`
4. Builds 7-day plan with {day, meals: {breakfast, lunch, dinner}} structure
5. Flattens unique food items across all meal types for recommendations list

**Frontend Rendering**:
1. DietPlan component receives `allDietPlans` array from ResultsPanel
2. Plans filtered (confidence ≥ 0.1%) and sorted by confidence descending
3. Tab buttons rendered for each plan
4. Active tab content shows: deficiency header → 7-day meal grid → food recommendation tags

**Tab Switching**:
1. User clicks alternative tab
2. `setActiveTab(index)` updates state
3. `activePlan = plans[index]` selected
4. Content re-renders with fade-in animation (key-based remount)

**Download Flow**:
1. User clicks "📥 Download All Diet Plans"
2. `generateDietPlanText()` iterates all plans, formatting each with headers, day-by-day meals
3. Text assembled as string with section separators
4. `Blob` created with `text/plain` MIME type
5. Temporary `<a>` element created with `download="diet_plans_all_deficiencies.txt"`
6. Programmatic click triggers browser download
7. Element removed from DOM, object URL revoked

---

## 3. Sequence Diagram 3 — Nearby Doctors Location Search

**Diagram**: [sequence3.puml](../diagrams/sequence3.puml)

### 3.1 Purpose
Covers the geolocation permission flow, Overpass API querying, map rendering, and doctor list interaction.

### 3.2 Flow Description

**Phase 1 — Location Request**:
1. NearbyDoctors renders in "idle" state with CTA card
2. User clicks "📍 Share My Location"
3. `navigator.geolocation.getCurrentPosition()` called with `enableHighAccuracy: true, timeout: 10000`
4. Browser prompts user for location permission
5. On grant: coordinates stored in state, location state → "granted"
6. On deny: error displayed, location state → "denied", retry button shown

**Phase 2 — Hospital Query**:
1. `useEffect` triggers when `userCoords` or `searchRadius` changes
2. Overpass API queried via HTTP POST with OverpassQL:
   - Searches for: `amenity=hospital`, `amenity=clinic`, `amenity=doctors`, `healthcare=doctor`, `healthcare=hospital`
   - Both `node` and `way` elements within the radius
3. Response filtered for named entries only
4. Pseudo-random ratings generated from OSM element IDs (deterministic)
5. Results sorted by rating, limited to 20

**Phase 3 — Map & List Rendering**:
1. Leaflet MapContainer renders with CartoDB dark tiles
2. User location shown as custom pulsing blue dot marker
3. Hospital markers placed using default Leaflet icons
4. FitBounds auto-adjusts viewport to show all markers
5. Doctor list renders below map with Haversine-calculated distances
6. Each card shows: type badge, name, star rating, review count, address, phone, distance

**Phase 4 — Interactions**:
1. Clicking map marker → popup with details, card highlighted in list
2. Changing radius dropdown → new Overpass query → updated results
3. Clicking website link → opens in new tab
4. Clicking doctor card → toggles selection state

### 3.3 Race Condition Prevention
The component uses a `cancelled` flag to prevent state updates from stale responses:
```javascript
let cancelled = false;
fetchNearbyDoctors(lat, lon, radius).then(results => {
    if (!cancelled) setDoctors(results);
});
return () => { cancelled = true; };
```

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
