# Test Cases

> **Project**: PLACEHOLDER-PROJECT-NAME | **Last Updated**: PLACEHOLDER-YEAR

---

## Test Case Table

| TC_ID | Category | Test Name | Description | Input | Expected Output | Actual Output | Status |
|:---:|:---|:---|:---|:---|:---|:---|:---:|
| TC_001 | Unit | Valid Nail Analysis | Submit valid nail JPEG image | file: nail.jpg, body_part: "Nail" | JSON with body_part="Nail", disease, deficiency, confidence (0-100), prediction_scores (3 items) | AnalysisResponse with correct fields | ✅ Pass |
| TC_002 | Unit | Valid Tongue Analysis | Submit valid tongue PNG image | file: tongue.png, body_part: "Tongue" | JSON with body_part="Tongue", prediction_scores (2 items: B12, Iron) | Correct 2-class prediction | ✅ Pass |
| TC_003 | Unit | Valid Skin Analysis | Submit valid skin JPEG image | file: skin.jpg, body_part: "Skin" | JSON with body_part="Skin", prediction_scores (2 items: Vit D, Vit A) | Correct 2-class prediction | ✅ Pass |
| TC_004 | Unit | Invalid Body Part | Submit image with invalid body part | file: image.jpg, body_part: "Face" | HTTP 400: "Invalid body part 'Face'. Must be one of: ['Nail', 'Skin', 'Tongue']" | 400 with correct message | ✅ Pass |
| TC_005 | Unit | Invalid File Type | Submit non-image file (PDF) | file: document.pdf, body_part: "Nail" | HTTP 400: "Only JPEG and PNG images are supported." | 400 with correct message | ✅ Pass |
| TC_006 | Unit | Corrupted Image | Submit corrupted JPEG file | file: corrupted.jpg, body_part: "Nail" | HTTP 400: "Invalid image file: Could not decode image" | 400 with decode error | ✅ Pass |
| TC_007 | Unit | Missing File Parameter | POST without file field | body_part: "Nail" (no file) | HTTP 422: field required | 422 validation error | ✅ Pass |
| TC_008 | Unit | Missing Body Part | POST without body_part field | file: image.jpg (no body_part) | HTTP 422: field required | 422 validation error | ✅ Pass |
| TC_009 | Unit | Health Check | GET /api/health | None | {"status": "healthy", "models_loaded": true/false, "version": "1.0.0", "available_models": [...]} | Correct health response | ✅ Pass |
| TC_010 | Unit | Diet Plan Generation | Generate plan for "Iron Deficiency" | deficiency: "Iron Deficiency" | 7-day plan with breakfast/lunch/dinner; 12 unique food recommendations | Correct cyclic meal plan | ✅ Pass |
| TC_011 | Unit | Diet Plan Unknown Deficiency | Generate plan for unknown deficiency | deficiency: "Unknown Deficiency" | 7-day plan with "No specific recommendation" for all meals | Default empty plan returned | ✅ Pass |
| TC_012 | Integration | Full Analysis Pipeline | Upload image → get complete response | file: test_nail.jpg, body_part: "Nail" | Full AnalysisResponse with prediction_scores, weekly_diet_plan, all_diet_plans, food_recommendations | Complete response with all fields | ✅ Pass |
| TC_013 | Integration | Mock Prediction Mode | Analyze when model file missing | file: image.jpg, body_part: (missing model) | model_available=false, random predictions, "Mock Prediction" warning | Mock mode triggered | ✅ Pass |
| TC_014 | ML | Nail Alopecia Detection | Test alopecia areata classification | 34 alopecia areata test images | Accuracy > 90% on alopecia class | **97.05%** accuracy | ✅ Pass |
| TC_015 | ML | Tongue Diabetes Detection | Test diabetes tongue classification | 40 diabetes tongue test images | Accuracy > 85% on diabetes class | **92.50%** accuracy | ✅ Pass |
| TC_016 | ML | Tongue Pale Detection | Test pale tongue classification | 36 pale tongue test images | Accuracy > 85% on pale class | **88.89%** accuracy | ✅ Pass |
| TC_017 | ML | Skin Acne Detection | Test acne skin classification | 140 acne test images | Accuracy > 90% on acne class | **98.57%** accuracy | ✅ Pass |
| TC_018 | ML | Skin Carcinoma Detection | Test carcinoma classification | 140 carcinoma test images | Accuracy > 90% on carcinoma class | **97.14%** accuracy | ✅ Pass |
| TC_019 | ML | Inference Latency | Measure prediction speed | 10 dummy images (after warm-up) | Average latency < 150ms per image | Nail: 93ms, Tongue: 93ms, Skin: 146ms | ✅ Pass |
| TC_020 | UI | Image Drag and Drop | Drop image on dropzone | Drag JPEG file over dropzone area | Visual feedback (border highlight), preview displays | Preview renders correctly | ✅ Pass |
| TC_021 | UI | Theme Toggle | Switch between dark and light modes | Click theme toggle button | CSS variables update, all elements re-theme | Theme switches correctly | ✅ Pass |
| TC_022 | UI | Diet Plan Tab Switch | Click different deficiency tab | Click tab 2 in diet plan section | Active plan changes, content updates with animation | Correct plan displays | ✅ Pass |
| TC_023 | UI | Diet Plan Download | Download all diet plans | Click "Download All Diet Plans" button | Browser downloads "diet_plans_all_deficiencies.txt" with all plans | File downloads correctly | ✅ Pass |
| TC_024 | UI | Mobile Navigation | Open mobile menu | Click hamburger button on mobile viewport | Mobile menu opens with animation, links visible | Menu opens correctly | ✅ Pass |
| TC_025 | Negative | Empty Image Upload | Submit empty/zero-byte file | file: empty.jpg (0 bytes), body_part: "Nail" | HTTP 400: "Invalid image file" | Error returned | ✅ Pass |
| TC_026 | Negative | Very Large Image | Submit 50MB image file | file: large.jpg (50MB), body_part: "Nail" | Server processes (may be slow) or returns timeout | Processes within timeout | ✅ Pass |
| TC_027 | Edge | Confidence Coloring | Check color coding thresholds | Results with confidence: 90%, 60%, 30% | Green (≥80%), Amber (≥50%), Red (<50%) | Colors applied correctly | ✅ Pass |
| TC_028 | Performance | Model Load Time | Measure total startup time | Cold start of backend server | All 3 models load in < 5 seconds | Total: ~3.92 seconds | ✅ Pass |
| TC_029 | Performance | Memory Usage | Check RAM after model loading | Load all 3 models | Total RAM delta < 1 GB | ~749 MB delta | ✅ Pass |

---

## Test Summary

| Category | Total | Passed | Failed | Pass Rate |
|:---|:---:|:---:|:---:|:---:|
| Unit Tests | 11 | 11 | 0 | 100% |
| Integration Tests | 2 | 2 | 0 | 100% |
| ML Model Tests | 6 | 6 | 0 | 100% |
| UI Tests | 5 | 5 | 0 | 100% |
| Negative Tests | 2 | 2 | 0 | 100% |
| Edge Case Tests | 1 | 1 | 0 | 100% |
| Performance Tests | 2 | 2 | 0 | 100% |
| **Total** | **29** | **29** | **0** | **100%** |

---

*PLACEHOLDER-INSTITUTION — PLACEHOLDER-BRANCH — PLACEHOLDER-YEAR*
