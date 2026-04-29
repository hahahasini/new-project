# State Diagrams

> **Project**: PLACEHOLDER-PROJECT-NAME — Vitamin Deficiency Detection System  
> **Version**: 1.0.0 | **Last Updated**: PLACEHOLDER-YEAR

---

## Overview

This document describes the state machines governing PLACEHOLDER-PROJECT-NAME's user sessions, analysis processing, diet plan interaction, nearby doctors flow, and theme management.

See also: [State Diagram](../diagrams/state.puml)

---

## 1. Application-Level State Machine

### States
| State | Description | Visual Indicator |
|:---|:---|:---|
| **Home Page** | User is browsing the landing page with model cards, stats, how-it-works | Hero section visible |
| **Analysis Page** | User is on a body-part-specific analysis page | Page header with body part title |

### Transitions
| From | To | Trigger |
|:---|:---|:---|
| Home Page | Analysis Page | Click "Analyze Now →" or navbar link |
| Analysis Page | Home Page | Click "← Back to Models" or logo/home link |
| Analysis Page | Analysis Page | Click different navbar analysis link |

---

## 2. Analysis Page State Machine

This is the core state machine governing the image analysis workflow on each analysis page (NailPage, TonguePage, SkinPage).

### States

| State | React State | UI Behavior |
|:---|:---|:---|
| **Idle** | `selectedImage=null, results=null, loading=false, error=null` | Dropzone visible, no buttons shown |
| **Image Selected** | `selectedImage=File, previewUrl=string, results=null, loading=false` | Image preview shown, "Analyze Image" and "Clear" buttons enabled |
| **Analyzing** | `selectedImage=File, results=null, loading=true` | Spinner on button, skeleton loading in results area, buttons disabled |
| **Results Displayed** | `selectedImage=File, results=AnalysisResponse, loading=false` | Full ResultsPanel with chart, diet, doctors |
| **Error** | `selectedImage=File, results=null, error=string` | Error card with message; image still selected for retry |

### Transitions

| From | To | Trigger | Action |
|:---|:---|:---|:---|
| Idle | Image Selected | File drag & drop or browse | `setSelectedImage(file)`, `setPreviewUrl(objectURL)` |
| Image Selected | Analyzing | Click "Analyze Image" | `setLoading(true)`, POST /api/analyze |
| Image Selected | Idle | Click "Clear" | Reset all state to initial |
| Analyzing | Results Displayed | API 200 response | `setResults(data)`, `setLoading(false)` |
| Analyzing | Error | API error or network failure | `setError(message)`, `setLoading(false)` |
| Error | Image Selected | (Implicit) | Image still selected; user can retry |
| Results Displayed | Idle | Click "Clear" | Reset all state to initial |
| Results Displayed | Image Selected | Select new image | New image replaces old; results cleared |

### State Conditions
- **Cannot transition Idle → Analyzing**: Image must be selected first
- **Cannot transition Analyzing → any user action**: Buttons disabled during loading
- **Error preserves image**: User doesn't need to re-upload to retry

---

## 3. Diet Plan Interaction States

| State | Description | React State |
|:---|:---|:---|
| **Tab 1 Active** | Highest-confidence deficiency plan displayed | `activeTab=0` |
| **Tab N Active** | Alternative deficiency plan displayed | `activeTab=N` |
| **Downloading** | Text file generation and browser download in progress | (Synchronous, no explicit state) |

### Transitions
| From | To | Trigger |
|:---|:---|:---|
| Tab 1 Active | Tab N Active | Click tab N |
| Tab N Active | Tab 1 Active | Click tab 1 |
| Any Tab | Downloading | Click "📥 Download All Diet Plans" |
| Downloading | Previous Tab | Download complete |

---

## 4. Nearby Doctors State Machine

The NearbyDoctors component implements a multi-stage state machine managing location permission, data fetching, and display.

### States

| State | `locationState` | UI Behavior |
|:---|:---|:---|
| **Location Idle** | `"idle"` | CTA card: "📍 Share My Location" with explanation text |
| **Requesting Location** | `"requesting"` | Button shows spinner + "Locating…" |
| **Location Granted** | `"granted"` | Triggers data fetching |
| **Location Denied** | `"denied"` | Error message + "🔄 Retry" button |
| **Location Error** | `"error"` | Error for unsupported browsers |
| **Fetching Doctors** | (granted + loading=true) | Map loading overlay with spinner |
| **Map Displayed** | (granted + loading=false + doctors.length > 0) | Interactive map + doctor list |
| **No Results** | (granted + loading=false + doctors.length === 0) | "No hospitals found" card |
| **Fetch Error** | (granted + fetchError) | Error card with retry |

### Transitions

| From | To | Trigger |
|:---|:---|:---|
| Location Idle | Requesting Location | Click "Share My Location" |
| Requesting Location | Location Granted | `getCurrentPosition` success callback |
| Requesting Location | Location Denied | `getCurrentPosition` error (code 1) |
| Requesting Location | Location Error | `getCurrentPosition` error (other) |
| Location Denied | Requesting Location | Click "🔄 Retry" |
| Location Granted | Fetching Doctors | `useEffect` auto-trigger |
| Fetching Doctors | Map Displayed | API returns results (length > 0) |
| Fetching Doctors | No Results | API returns empty results |
| Fetching Doctors | Fetch Error | API request fails |
| Map Displayed | Fetching Doctors | Radius changed |
| No Results | Fetching Doctors | Radius changed |

### Timeout & Session Management
- Geolocation timeout: 10,000 ms (10 seconds)
- Maximum position age: 60,000 ms (cached positions up to 1 minute old)
- No session persistence — location state resets on page navigation

---

## 5. Theme State Machine

The simplest state machine in the application, managing dark/light mode.

| State | `theme` | CSS Effect |
|:---|:---|:---|
| **Light Mode** | `"light"` | Default colors via CSS custom properties |
| **Dark Mode** | `"dark"` | `[data-theme="dark"]` CSS selector activates dark palette |

### Transitions
| From | To | Trigger |
|:---|:---|:---|
| Light Mode | Dark Mode | Click moon icon (🌙) |
| Dark Mode | Light Mode | Click sun icon (☀️) |

### Initialization
- **Always starts in Light Mode** on page load (no localStorage persistence)
- Theme attribute applied via `document.documentElement.setAttribute('data-theme', theme)` in a `useEffect`

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
