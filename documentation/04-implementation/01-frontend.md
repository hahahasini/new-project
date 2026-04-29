# Frontend Implementation

> **Project**: PLACEHOLDER-PROJECT-NAME — Vitamin Deficiency Detection System  
> **Technology**: React 18.3.1 + Vite 5.4.0 | **Language**: JavaScript (JSX)

---

## 1. Component Architecture

### 1.1 Top-Level Structure
```
frontend/src/
├── App.jsx              # Root router with Layout wrapper
├── main.jsx             # ReactDOM render entry point
├── App.css              # Global styles (~54KB, comprehensive design system)
├── index.css            # Base reset and root variables (~8KB)
├── components/          # Reusable UI components
│   ├── Navbar.jsx       # Responsive navigation bar with theme toggle
│   ├── Footer.jsx       # Page footer
│   ├── ImageUploader.jsx    # Drag-and-drop image selection
│   ├── ResultsPanel.jsx     # Analysis results orchestrator
│   ├── ConfidenceChart.jsx  # Chart.js bar chart
│   ├── DietPlan.jsx         # Tabbed weekly diet plans
│   ├── NearbyDoctors.jsx    # Geolocation + map + doctor list
│   ├── BodyPartSelector.jsx # Body part selection UI
│   └── Header.jsx           # Page header component
├── pages/               # Route-level page components
│   ├── HomePage.jsx     # Landing page with model cards
│   ├── NailPage.jsx     # Nail analysis page
│   ├── TonguePage.jsx   # Tongue analysis page
│   └── SkinPage.jsx     # Skin analysis page
├── services/            # API communication
│   └── api.js           # Axios client with analyzeImage/healthCheck
├── contexts/            # Global state providers
│   └── ThemeContext.jsx  # Dark/light mode context
└── assets/              # Static assets
```

### 1.2 Component Hierarchy
```
<BrowserRouter>                    (main.jsx)
  <ThemeProvider>                  (ThemeContext.jsx)
    <App>                          (App.jsx)
      <Routes>
        <Route element={<Layout>}>
          <Navbar />               (Navbar.jsx - always visible)
          <Outlet>                 (renders active page)
            <HomePage />          (or NailPage/TonguePage/SkinPage)
          </Outlet>
          <Footer />              (Footer.jsx - always visible)
        </Route>
      </Routes>
    </App>
  </ThemeProvider>
</BrowserRouter>
```

---

## 2. State Management

### 2.1 Local Component State (useState)
Each analysis page manages its own isolated state:

```javascript
function NailPage() {
    const [selectedImage, setSelectedImage] = useState(null);   // File object
    const [previewUrl, setPreviewUrl] = useState(null);         // Blob URL string
    const [results, setResults] = useState(null);               // API response
    const [loading, setLoading] = useState(false);              // Analysis in progress
    const [error, setError] = useState(null);                   // Error message
    // ...
}
```

**Design Decision**: Each analysis page (NailPage, TonguePage, SkinPage) maintains independent state. This prevents cross-contamination between analyses and simplifies component logic. The trade-off is that navigating between pages resets state, which is acceptable since users typically analyze one body part at a time.

### 2.2 Global State (React Context)
Theme state is shared globally via Context API:

```javascript
const ThemeContext = createContext();

export function ThemeProvider({ children }) {
    const [theme, setTheme] = useState('light');  // Always start light
    
    useEffect(() => {
        document.documentElement.setAttribute('data-theme', theme);
    }, [theme]);
    
    const toggleTheme = () => setTheme(t => (t === 'dark' ? 'light' : 'dark'));
    
    return (
        <ThemeContext.Provider value={{ theme, toggleTheme }}>
            {children}
        </ThemeContext.Provider>
    );
}
```

**Design Decision**: Context API was chosen over Redux because only theme state needs global access. The lightweight approach avoids unnecessary dependencies and boilerplate.

---

## 3. Routing Structure

| Route | Component | Description |
|:---|:---|:---|
| `/` | `HomePage` | Landing page with model cards, stats, workflow steps |
| `/nail` | `NailPage` | Nail deficiency analysis (Iodine, Vitamin D) |
| `/tongue` | `TonguePage` | Tongue deficiency analysis (B12, Iron) |
| `/skin` | `SkinPage` | Skin deficiency analysis (Vitamin D, Vitamin A) |

**Layout Pattern**: All routes share a common layout with persistent Navbar and Footer via React Router's `<Outlet />`:

```jsx
function Layout() {
    return (
        <div className="app">
            <Navbar />
            <div className="page-outlet"><Outlet /></div>
            <Footer />
        </div>
    );
}
```

---

## 4. Key Interactive Features

### 4.1 Drag-and-Drop Image Upload (ImageUploader.jsx)
The ImageUploader implements a full drag-and-drop interface with fallback file browser:

```jsx
// Drag events manage visual feedback
const handleDragOver  = (e) => { e.preventDefault(); setDragOver(true); };
const handleDragLeave = (e) => { e.preventDefault(); setDragOver(false); };

const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) onImageSelect(file);
};
```

**Key behaviors**: Visual feedback during drag (`drag-over` class), file type validation, hidden `<input>` for click-to-browse, keyboard accessibility (`tabIndex={0}`, Enter key handler).

### 4.2 Confidence Chart (ConfidenceChart.jsx)
Uses Chart.js via `react-chartjs-2` to render per-class confidence scores:

```jsx
const data = {
    labels: sortedScores.map(s => s.label),
    datasets: [{
        label: 'Confidence (%)',
        data: sortedScores.map(s => s.confidence),
        backgroundColor: ['rgba(99,102,241,0.6)', ...],
        borderRadius: 6,
    }],
};
```

**Configuration**: Responsive, 1.8:1 aspect ratio, sorted descending, dark-theme tooltips, percentage Y-axis (0–100%).

### 4.3 Interactive Map (NearbyDoctors.jsx)
The most complex component (~430 lines), integrating multiple APIs:

1. **Browser Geolocation** → user coordinates
2. **Overpass API** → nearby hospital/clinic data
3. **Leaflet** → interactive map with markers
4. **Haversine** → distance calculations

```jsx
// Overpass query for nearby medical facilities
const query = `
    [out:json][timeout:25];
    (
        node["amenity"="hospital"](around:${radius},${lat},${lon});
        node["amenity"="clinic"](around:${radius},${lat},${lon});
        // ...
    );
    out body center 30;
`;
```

---

## 5. Styling Approach

### 5.1 CSS Design System
The application uses a comprehensive vanilla CSS design system with:

- **CSS Custom Properties**: Colors, spacing, typography, border radii defined as variables
- **`[data-theme="dark"]`**: Dark mode overrides all color variables
- **Animations**: Fade-in, slide-in, stagger effects via CSS keyframes
- **Glassmorphism**: `.glass` class with backdrop-blur and translucent backgrounds
- **Responsive**: Media queries for mobile, tablet, desktop breakpoints

### 5.2 CSS File Structure
| File | Size | Purpose |
|:---|:---:|:---|
| `index.css` | 8.2 KB | CSS reset, root variables, base typography |
| `App.css` | 54.7 KB | Complete design system, all component styles |

### 5.3 Theme Implementation
```css
:root {
    --bg-primary: #ffffff;
    --text-primary: #1a1a2e;
    /* ... */
}

[data-theme="dark"] {
    --bg-primary: #0f0f23;
    --text-primary: #e2e8f0;
    /* ... */
}
```

---

## 6. Performance Optimizations

| Technique | Implementation |
|:---|:---|
| Lazy image loading | `loading="lazy"` on model card images |
| Client-side preview | `URL.createObjectURL` avoids server upload for preview |
| Skeleton loading | Placeholder blocks during analysis wait |
| CSS animations | GPU-accelerated transforms and opacity transitions |
| Staggered children | `animation-delay` prevents simultaneous rendering load |
| Chart.js tree-shaking | Only imports used chart types (Bar, CategoryScale, etc.) |
| Race condition prevention | `cancelled` flag in useEffect cleanup |

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
