# Database Implementation

> **Project**: PLACEHOLDER-PROJECT-NAME | **Architecture**: Configuration-Driven (No Traditional Database)

---

## 1. Data Storage Approach

PLACEHOLDER-PROJECT-NAME uses a **configuration-driven data model** rather than a traditional RDBMS or NoSQL database. All domain data is stored in Python dictionaries within `config.py`, loaded into memory at module import time.

### 1.1 Rationale
| Factor | Decision |
|:---|:---|
| **Data Volume** | Fixed domain data (~14 deficiency categories, 3 body parts) — no user-generated data |
| **Read/Write Pattern** | Read-only at runtime; data changes only during development |
| **Latency** | In-memory dictionary lookup (~O(1)) vs database query overhead |
| **Deployment Simplicity** | No database server to configure, maintain, or back up |
| **Privacy** | No persistent storage means no data breach risk |
| **Statelesness** | Each request is independent; no session or user data |

### 1.2 Data Structures

**CLASSES Dictionary** — Maps body parts to deficiency labels (index-aligned with model output):
```python
CLASSES = {
    "Nail":   ["No Vitamin Deficiency", "Iodine Deficiency", "Vitamin D Deficiency"],
    "Tongue": ["Vitamin B12 Deficiency", "Iron Deficiency"],
    "Skin":   ["Vitamin D Deficiency", "Vitamin A Deficiency"],
}
```

**DISEASES Dictionary** — Maps body parts to disease labels:
```python
DISEASES = {
    "Nail":   ["No disease", "Bluish nails", "Aloperia areata"],
    "Tongue": ["Diabetes", "Pale tongue"],
    "Skin":   ["Acne", "Carcinoma"],
}
```

**FOOD_RECOMMENDATIONS Dictionary** — 14 deficiency categories, each with breakfast/lunch/dinner arrays (3-4 items each). Total: ~168 unique meal recommendations across 42 meal slots.

---

## 2. Schema Definition

### 2.1 Logical Schema (Python Dictionaries)

```
Settings
├── APP_NAME: str
├── APP_VERSION: str
├── MODELS_DIR: Path
├── NAIL_MODEL: str
├── TONGUE_MODEL: str
├── SKIN_MODEL: str
├── DEFAULT_IMG_SIZE: (int, int)
└── CORS_ORIGINS: list[str]

CLASSES: dict[str, list[str]]
├── "Nail" → [3 deficiency labels]
├── "Tongue" → [2 deficiency labels]
└── "Skin" → [2 deficiency labels]

DISEASES: dict[str, list[str]]
├── "Nail" → [3 disease labels]
├── "Tongue" → [2 disease labels]
└── "Skin" → [2 disease labels]

FOOD_RECOMMENDATIONS: dict[str, dict[str, list[str]]]
├── "Vitamin A Deficiency" → {breakfast: [...], lunch: [...], dinner: [...]}
├── "Iron Deficiency" → {breakfast: [...], lunch: [...], dinner: [...]}
└── ... (14 total entries)
```

### 2.2 Access Patterns

| Operation | Implementation | Complexity |
|:---|:---|:---:|
| Get deficiency label by index | `CLASSES[body_part][index]` | O(1) |
| Get disease label by index | `DISEASES[body_part][index]` | O(1) |
| Get food recommendations | `FOOD_RECOMMENDATIONS.get(deficiency, {})` | O(1) |
| Get meal for day | `foods["breakfast"][i % len(foods["breakfast"])]` | O(1) |
| Flatten unique foods | `for item in foods.get(meal, [])` iteration | O(n) |

---

## 3. Indexing Strategy

Since the data model is in-memory Python dictionaries, traditional database indexing doesn't apply. However, the data is structured for optimal access:

| Access Pattern | Structure | Lookup Type |
|:---|:---|:---|
| Body part → classes | Top-level dict key | Hash table O(1) |
| Deficiency → foods | Top-level dict key | Hash table O(1) |
| Day → meal | Array index (cyclic) | Direct index O(1) |

---

## 4. Data Consistency

- **Immutability**: All data is defined at module level and never modified at runtime
- **Index Alignment**: `CLASSES[part][i]` and `DISEASES[part][i]` must share the same index for correct mapping
- **Validation**: Pydantic models enforce type constraints on API responses
- **No ACID concerns**: No transactions, no concurrent writes, no consistency issues

---

## 5. Future Database Integration

If user accounts or history tracking are added (see `suggestions.md` Future Enhancements), the recommended database would be:

| Aspect | Recommendation |
|:---|:---|
| **Database** | PostgreSQL 15+ |
| **ORM** | SQLAlchemy 2.0 with async support |
| **Tables** | users, analysis_history, diet_plans_saved |
| **Migration** | Alembic for schema versioning |
| **Connection** | asyncpg with connection pooling |

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
