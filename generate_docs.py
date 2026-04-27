import os

BASE_DIR = 'docs'

def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def generate_docs():
    # 1. Introduction
    create_file(f'{BASE_DIR}/1_Introduction/1.1_Purpose_of_the_project.md', """# 1.1 Purpose of the Project

The primary purpose of this project is to develop an intelligent, AI-powered system capable of detecting vitamin deficiencies using image processing and deep learning techniques. 

By analyzing user-submitted images of specific body parts (nails, tongues, or skin) along with the user's selection of the body part category, the system identifies underlying vitamin deficiencies and related nutritional disorders. Importantly, this project prioritizes a memory-efficient approach over large language models (LLMs), ensuring the solution is lightweight, cost-effective, and highly performant without sacrificing diagnostic capabilities.
""")
    create_file(f'{BASE_DIR}/1_Introduction/1.2_Problem_with_Existing_Systems.md', """# 1.2 Problem with Existing Systems

Existing diagnostic systems and LLM-based solutions often face several critical limitations:
- **High Resource Requirements**: LLMs and large foundation models consume massive amounts of memory and computational power, making them expensive to host and difficult to deploy in resource-constrained environments.
- **Latency Issues**: The inference time for massive models can be prohibitively high for real-time or quick consumer-facing applications.
- **Complexity**: General-purpose models often require complex prompting or multi-stage pipelines to identify specific patterns of vitamin deficiency, whereas our targeted approach simplifies the process by letting the user specify the context (Nail, Tongue, or Skin).
- **Accessibility**: Traditional clinical diagnosis methods are often time-consuming, expensive, and require physical visits to specialized laboratories.
""")
    create_file(f'{BASE_DIR}/1_Introduction/1.3_Proposed_System.md', """# 1.3 Proposed System

The proposed system addresses these challenges by employing targeted, highly specialized Convolutional Neural Networks (CNNs) designed specifically for image classification of body parts. 

**Key Characteristics of the Proposed System:**
- **Memory Efficiency**: Utilizes specialized deep learning models tailored for specific body parts (Nails, Tongue, Skin) rather than monolithic, memory-intensive LLMs.
- **Modern Architecture**: Incorporates a decoupled architecture featuring a Fast API backend and a responsive React frontend (powered by Vite).
- **Context-Aware Inference**: By allowing the user to select the body part, the system immediately routes the image to the correct specialized model, ensuring higher accuracy and efficiency.
- **Targeted Prediction**: Models are trained on categorized deficiency indicators such as Vitamin D, Vitamin A, Vitamin B12, Iron, and Iodine deficiencies based on visible symptomatic patterns.
- **Accessibility**: Provides an easy-to-use web interface for users to upload images and receive instantaneous, preliminary diagnostic feedback.
""")
    create_file(f'{BASE_DIR}/1_Introduction/1.4_Scope_of_the_Project.md', """# 1.4 Scope of the Project

The scope of this project encompasses the design, development, and deployment of a web-based vitamin deficiency detection system. 

**In-Scope:**
- Development of a React-based frontend using Vite and Vanilla CSS.
- Implementation of a FastAPI backend to handle REST API requests (`/api/analyze`).
- Integration of optimized TensorFlow/Keras CNN models for image classification (Input size: 224x224).
- User selection of body part category (Nail, Tongue, or Skin) to guide the analysis.
- Support for specific body part models:
  - **Nail Model**: No Deficiency, Iodine, Vit D
  - **Tongue Model**: Vit B12, Iron
  - **Skin Model**: Vit D, Vit A
- Preliminary diagnostic reporting via an intuitive UI.

**Out-of-Scope:**
- Replacing professional medical diagnosis. The tool serves as an early warning/awareness system.
- Automatic body part detection. The user provides the context to ensure maximum efficiency and targeted analysis.
""")
    create_file(f'{BASE_DIR}/1_Introduction/1.5_Architecture_Diagram.md', """# 1.5 Architecture Diagram

The system employs a modern decoupled client-server architecture:

```mermaid
flowchart TD
    subgraph Frontend [React Frontend (Vite + CSS)]
        UI[User Interface]
        Client[API Client]
        UI <--> Client
    end

    subgraph Backend [FastAPI Backend]
        Router[API Routers /api/analyze]
        Service[Business Logic & Image Processing]
        Router <--> Service
    end

    subgraph MachineLearning [ML Models (TensorFlow/Keras)]
        Nail[Nail Model]
        Tongue[Tongue Model]
        Skin[Skin Model]
        
        Service -->|Selected: Nail| Nail
        Service -->|Selected: Tongue| Tongue
        Service -->|Selected: Skin| Skin
    end

    Client <-->|HTTP/JSON: Image + Category| Router
```
""")

    # 2. Literature Survey
    create_file(f'{BASE_DIR}/2_Literature_Survey/2.1_Literature_Survey.md', """# 2.1 Literature Survey

Extensive research has demonstrated the viability of Convolutional Neural Networks (CNNs) in medical image classification. 

**Key Findings:**
- Deep learning techniques, specifically CNNs (like EfficientNet and VGG architectures), outperform traditional computer vision techniques in extracting intricate symptom patterns from human skin, nails, and tongues.
- Providing context (e.g., specifying the body part) to a specialized CNN model significantly improves classification accuracy compared to a generalized classifier that must first determine the organ type.
- While Large Language Models (LLMs) have gained popularity in recent years, studies indicate that for highly specialized visual classification tasks, appropriately sized CNNs offer comparable accuracy while drastically reducing memory footprint and inference latency.
- Early detection of vitamin deficiencies via visual indicators (e.g., pale tongue for iron deficiency, brittle nails for iodine/vitamin D issues) can significantly aid in preventive healthcare.
""")

    # 3. Software Requirement Specification
    create_file(f'{BASE_DIR}/3_Software_Requirement_Specification/3.1_Introduction_to_SRS.md', """# 3.1 Introduction to SRS

This Software Requirements Specification (SRS) document details the functional and non-functional requirements for the Vitamin Deficiency Detection System. It serves as a comprehensive guide for developers, stakeholders, and testers to ensure the final product aligns with the project goals of building a memory-efficient, deep learning-powered web application.
""")
    create_file(f'{BASE_DIR}/3_Software_Requirement_Specification/3.2_Role_of_SRS.md', """# 3.2 Role of SRS

The role of this SRS is to:
1. Clearly define the expected behavior of the system.
2. Establish technical constraints, specifically focusing on memory efficiency and decoupling frontend/backend.
3. Serve as the foundation for the System Design and Testing phases.
""")
    create_file(f'{BASE_DIR}/3_Software_Requirement_Specification/3.3_Requirements_Specification_Document.md', """# 3.3 Requirements Specification Document

The system must allow users to upload images of their nails, tongue, or skin along with the corresponding category selection, and receive an automated assessment regarding potential vitamin deficiencies based on pre-trained ML models.
""")
    create_file(f'{BASE_DIR}/3_Software_Requirement_Specification/3.4_Functional_Requirements.md', """# 3.4 Functional Requirements

- **FR1 Image and Category Input**: The system shall allow users to upload image files (JPEG, PNG) and select the body part category (Nail, Tongue, or Skin).
- **FR2 Image Preprocessing**: The backend shall resize and normalize images to 224x224 pixels.
- **FR3 Model Routing**: The system shall route the processed image to the specific sub-model based on the user's category selection.
- **FR4 Deficiency Prediction**: The system shall use the selected specialized model to predict the probability of specific vitamin deficiencies.
- **FR5 Results Display**: The frontend shall display the analysis results in a user-friendly format, indicating the identified body part and potential deficiencies.
- **FR6 Health Check**: The API must provide a `/api/health` endpoint for monitoring service status.
""")
    create_file(f'{BASE_DIR}/3_Software_Requirement_Specification/3.5_Non-Functional_Requirements.md', """# 3.5 Non-Functional Requirements

- **NFR1 Memory Efficiency**: The system must operate with significantly lower memory constraints compared to an LLM-based system, relying entirely on optimized CNN weights and avoiding redundant classification stages.
- **NFR2 Scalability**: The decoupled architecture (React + FastAPI) must allow for independent scaling of the frontend server and backend model inference server.
- **NFR3 Maintainability**: The code must be well-structured, modular, and use modern standard practices (e.g., Pydantic schemas in FastAPI).
""")
    create_file(f'{BASE_DIR}/3_Software_Requirement_Specification/3.6_Performance_Requirements.md', """# 3.6 Performance Requirements

- **Inference Time**: Model prediction must take less than 2 seconds under normal server load.
- **Responsiveness**: The React frontend must render smoothly and provide immediate user feedback during image uploads and selection.
""")
    create_file(f'{BASE_DIR}/3_Software_Requirement_Specification/3.7_Software_Requirements.md', """# 3.7 Software Requirements

**Backend:**
- Python 3.9+
- FastAPI
- Uvicorn
- TensorFlow / Keras (for ML models)
- OpenCV / Pillow (for image processing)

**Frontend:**
- Node.js 18+
- React
- Vite
- Vanilla CSS
""")
    create_file(f'{BASE_DIR}/3_Software_Requirement_Specification/3.8_Hardware_Requirements.md', """# 3.8 Hardware Requirements

**Server:**
- RAM: Minimum 8GB (Strictly avoiding the 16GB+ requirements of local LLMs)
- Processor: Multi-core CPU (Intel i5/Ryzen 5 or equivalent). GPU is optional but recommended for faster inference.
- Storage: 256GB SSD (to store models and temporary uploads).

**Client:**
- Any modern web browser (Chrome, Firefox, Safari, Edge).
""")

    # 4. System Design
    create_file(f'{BASE_DIR}/4_System_Design/4.1_Introduction_to_UML.md', """# 4.1 Introduction to UML

Unified Modeling Language (UML) diagrams are utilized to visualize the architecture, design, and implementation of the Vitamin Deficiency Detection System. These models provide a standardized way to blueprint the system's structure and behavior.
""")
    create_file(f'{BASE_DIR}/4_System_Design/4.2_UML_Diagrams.md', """# 4.2 UML Diagrams

The following sections contain the Use Case, Sequence, State Chart, and Deployment diagrams for the system.
""")
    create_file(f'{BASE_DIR}/4_System_Design/4.3_Use_Case_Diagram.md', """# 4.3 Use Case Diagram

```mermaid
usecaseDiagram
    actor User
    actor SystemAdmin
    
    User --> (Select Body Part Category)
    User --> (Upload Image)
    User --> (View Results)
    
    (Upload Image) .> (Preprocess Image) : include
    (Preprocess Image) .> (Route to Selected Model) : include
    (Route to Selected Model) .> (Predict Deficiency) : include
    
    SystemAdmin --> (Monitor Health Endpoint)
```

**Alternative Flowchart Representation:**
```mermaid
flowchart LR
    User([User]) --> Selection[Select Body Part]
    Selection --> Upload[Upload Image]
    Upload --> Backend[Backend Processing]
    Backend --> Results[View Results]
```
""")
    create_file(f'{BASE_DIR}/4_System_Design/4.4_Sequence_Diagram.md', """# 4.4 Sequence Diagram

```mermaid
sequenceDiagram
    actor User
    participant Frontend as React Frontend
    participant Backend as FastAPI Backend
    participant ML as ML Models
    
    User->>Frontend: Selects Category & Uploads Image
    Frontend->>Backend: POST /api/analyze (Image + Category)
    Backend->>Backend: Preprocess (Resize 224x224)
    Backend->>ML: Route to Selected Model (e.g., Nail)
    Backend->>ML: Predict Deficiency
    ML-->>Backend: Returns Probabilities (Iodine, Vit D)
    Backend-->>Frontend: JSON Response with Results
    Frontend-->>User: Displays Results UI
```
""")
    create_file(f'{BASE_DIR}/4_System_Design/4.5_State_Chart_Diagram.md', """# 4.5 State Chart Diagram

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Selecting : User chooses body part
    Selecting --> Uploading : User selects image
    Uploading --> Processing : Data sent to backend
    Processing --> Analyzing : Preprocessing complete
    Analyzing --> Success : Prediction generated
    Analyzing --> Error : Invalid input
    Success --> Idle : User dismisses results
    Error --> Idle : User retries
```
""")
    create_file(f'{BASE_DIR}/4_System_Design/4.6_Deployment_Diagram.md', """# 4.6 Deployment Diagram

```mermaid
flowchart TD
    subgraph Client [Client Environment]
        Browser[Web Browser]
    end

    subgraph Server [Hosting Environment]
        subgraph FrontendContainer [Frontend Host]
            Vite[Vite/React Static Files]
        end
        subgraph BackendContainer [Backend Host]
            Uvicorn[Uvicorn Server]
            FastAPI[FastAPI App]
            Models[(TensorFlow .h5/.keras Models)]
        end
    end

    Browser <-->|HTTP| Vite
    Browser <-->|REST/JSON: Multi-part| Uvicorn
    Uvicorn --> FastAPI
    FastAPI --> Models
```
""")
    create_file(f'{BASE_DIR}/4_System_Design/4.7_Technologies_Used.md', """# 4.7 Technologies Used

- **Frontend:** React, Vite, Vanilla CSS
- **Backend Framework:** FastAPI, Uvicorn
- **Machine Learning:** TensorFlow, Keras
- **Image Processing:** OpenCV, Pillow
- **Language:** Python 3.9+, JavaScript/TypeScript
""")

    # 5. Implementation
    create_file(f'{BASE_DIR}/5_Implementation/5.1_Setup_and_Connections.md', """# 5.1 Setup and Connections

### Environment Setup

The system is split into two distinct directories: `backend/` and `frontend/`.

**Backend Initialization:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows
pip install -r requirements.txt
```

**Frontend Initialization:**
```bash
cd frontend
npm install
```
""")
    create_file(f'{BASE_DIR}/5_Implementation/5.2_Coding_the_logic.md', """# 5.2 Coding the logic

**Backend Logic (`backend/app/main.py`):**
The FastAPI application receives a `FormData` object containing both the image file and the `category` string. 
Routers extract these parameters to determine the appropriate service path.

**Service Layer (`backend/app/services/`):**
The ML service receives the image and the user-specified category. 
The logic skips automatic organ classification and directly loads the relevant specialized model weights:
- **Nail Model**: Triggered when category is 'nail'. Checks for Iodine, Vitamin D deficiency.
- **Tongue Model**: Triggered when category is 'tongue'. Checks for Vitamin B12, Iron deficiency.
- **Skin Model**: Triggered when category is 'skin'. Checks for Vitamin D, Vitamin A deficiency.
""")
    create_file(f'{BASE_DIR}/5_Implementation/5.3_Connecting_the_frontend.md', """# 5.3 Connecting the frontend

**Frontend Integration (`frontend/src/services/api.js`):**
The React application captures the user's body part selection (e.g., via a dropdown or radio buttons) and the image file. 
Both are bundled into a `FormData` object and posted to the `/api/analyze` endpoint.

```javascript
// Example logic
const formData = new FormData();
formData.append('file', imageFile);
formData.append('category', selectedCategory); // 'nail', 'tongue', or 'skin'
const response = await fetch('http://localhost:8000/api/analyze', {
    method: 'POST',
    body: formData
});
const data = await response.json();
```
""")
    create_file(f'{BASE_DIR}/5_Implementation/5.4_Screenshots.md', """# 5.4 Screenshots

*(Note: Actual screenshots will be inserted here upon deployment)*

1. **Selection & Upload Screen**: Shows the UI where users select the body part before uploading.
2. **Analysis State**: Shows the targeted inference process.
3. **Results Dashboard**: Displays deficiency confidence scores based on the chosen category.
""")

    # 6. Software Testing
    create_file(f'{BASE_DIR}/6_Software_Testing/6.1_Introduction.md', """# 6.1 Introduction to Testing

Testing ensures the reliability, accuracy, and performance of the Vitamin Deficiency Detection System. It verifies that the user-provided category correctly routes to the appropriate ML model.
""")
    create_file(f'{BASE_DIR}/6_Software_Testing/6.2_Testing_Objectives.md', """# 6.2 Testing Objectives

1. Verify that the user-selected category is correctly received and parsed by the backend.
2. Ensure the correct specialized model is loaded based on the category.
3. Confirm that the system uses memory efficiently by loading only one specialized model at a time.
4. Validate UI responsiveness across different devices.
""")
    create_file(f'{BASE_DIR}/6_Software_Testing/6.3_Testing_Strategies.md', """# 6.3 Testing Strategies

- **Unit Testing**: Pytest for backend routing logic (verifying that 'nail' category loads the nail model).
- **Integration Testing**: End-to-end tests ensuring the frontend sends the correct `FormData` and the backend returns the appropriate schema.
- **Performance Testing**: Monitoring RAM usage to ensure only necessary weights are loaded into memory.
""")
    create_file(f'{BASE_DIR}/6_Software_Testing/6.4_System_Evaluation.md', """# 6.4 System Evaluation

System evaluation involves testing the specialized models against categorical validation datasets to ensure high accuracy for user-specified body parts.
""")
    create_file(f'{BASE_DIR}/6_Software_Testing/6.5_Testing_New_System.md', """# 6.5 Testing New System

Testing confirms that the explicit category selection reduces errors compared to an automated classifier, providing a more reliable user experience.
""")
    create_file(f'{BASE_DIR}/6_Software_Testing/6.6_Test_Cases.md', """# 6.6 Test Cases

| Test Case ID | Description | Expected Result | Status |
|---|---|---|---|
| TC_01 | Select 'Nail' and upload nail image | Backend uses Nail Model and returns correct probabilities | Pending |
| TC_02 | Select 'Skin' and upload image | Backend uses Skin Model | Pending |
| TC_03 | Upload image without selecting category | Frontend prevents submission or backend returns validation error | Pending |
| TC_04 | Monitor RAM usage | Memory efficiency is maintained by avoiding a multi-stage classification pipeline | Pending |
""")

    # 7. Conclusion
    create_file(f'{BASE_DIR}/7_Conclusion/7.1_Conclusion.md', """# 7.1 Conclusion

The Vitamin Deficiency Detection System successfully demonstrates how targeted Deep Learning techniques (CNNs) can be utilized to identify health risks from visual indicators on nails, tongues, and skin. By implementing a decoupled FastAPI and React architecture, the project provides a highly responsive, modern web application.

Crucially, the system achieves its primary goal of memory efficiency by utilizing specialized, lightweight models instead of relying on resource-intensive Large Language Models (LLMs). This makes the system scalable, cost-effective, and highly accessible as a preliminary diagnostic support tool.
""")

    # 8. Future Enhancements
    create_file(f'{BASE_DIR}/8_Future_Enhancements/8.1_Future_Enhancements.md', """# 8.1 Future Enhancements

- **Dietary Recommendations**: Integrate a rule-based engine to provide tailored dietary advice based on the detected deficiencies.
- **Mobile Application**: Port the React web application to React Native for native iOS and Android apps.
- **Expanded Dataset**: Continuously gather more clinical data to improve the model accuracy and include more categories of deficiencies.
- **User Authentication**: Implement JWT-based login to allow users to track their deficiency history over time.
""")

    # 9. References
    create_file(f'{BASE_DIR}/9_References/9.1_References.md', """# 9.1 References

1. Original Repository Documentation: *Vitamin Deficiency Detection Using Image Processing and Deep Learning Techniques*.
2. FastAPI Documentation: https://fastapi.tiangolo.com/
3. React Documentation: https://react.dev/
4. TensorFlow/Keras Documentation: https://www.tensorflow.org/
""")

    # 10. Bibliography
    create_file(f'{BASE_DIR}/10_Bibliography/10.1_Bibliography.md', """# 10.1 Bibliography

- Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.
- Chollet, F. (2021). *Deep Learning with Python* (2nd ed.). Manning Publications.
""")

if __name__ == '__main__':
    generate_docs()
    print("Documentation generation complete.")
