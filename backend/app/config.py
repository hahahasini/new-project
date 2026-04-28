import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable overrides."""

    APP_NAME: str = "Vitamin Deficiency Detection API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Base paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    MODELS_DIR: Path = BASE_DIR / "models"

    # Model file names (only models that actually exist)
    NAIL_MODEL: str = "nail/Nail_epoch_24.keras"
    TONGUE_MODEL: str = "tongue/Tongue_epoch_01.keras"
    SKIN_MODEL: str = "skin/skin_disease_model_epoch_46.keras"

    # Image preprocessing
    DEFAULT_IMG_SIZE: tuple = (224, 224)

    # CORS
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# ---------------------------------------------------------------------------
# Domain data: class labels, disease mappings, food recommendations
# ---------------------------------------------------------------------------

BODY_PARTS = ["Nail", "Skin", "Tongue"]
ALL_BODY_PARTS = ["Nail", "Skin", "Tongue"]  # Full list for reference

# Models that are available on disk
AVAILABLE_MODELS = {"Nail", "Skin", "Tongue"}

CLASSES = {
    "Nail": ["No Vitamin Deficiency", "Iodine Deficiency", "Vitamin D Deficiency"],
    "Tongue": ["Vitamin B12 Deficiency", "Iron Deficiency"],
    "Skin": ["Vitamin D Deficiency", "Vitamin A Deficiency"],
}

DISEASES = {
    "Nail": ["No disease", "Bluish nails", "Aloperia areata"],
    "Tongue": ["Diabetes", "Pale tongue"],
    "Skin": ["Acne", "Carcinoma"],
}

FOOD_RECOMMENDATIONS = {
    "Vitamin A Deficiency": {
        "breakfast": [
            "Oatmeal with grated carrots and cinnamon", 
            "Spinach and apple smoothie with chia seeds", 
            "Sweet potato hash with bell peppers", 
            "Rice porridge with baked pumpkin"
        ],
        "lunch": [
            "Lentil and spinach stew", 
            "Roasted sweet potato and black bean bowl", 
            "Carrot and ginger soup with quinoa", 
            "Kale and roasted butternut squash salad"
        ],
        "dinner": [
            "Broccoli and carrot stir-fry with rice", 
            "Baked sweet potato topped with black beans", 
            "Spinach and chickpea curry", 
            "Pumpkin and sage risotto (dairy-free)"
        ]
    },
    "Vitamin B Deficiency": {
        "breakfast": [
            "Quinoa bowl with sliced bananas", 
            "Oatmeal with sunflower seeds and berries", 
            "Rice flakes with fortified plant milk", 
            "Millet porridge with chopped apples"
        ],
        "lunch": [
            "Black bean and corn salad", 
            "Lentil soup with mixed vegetables", 
            "Chickpea and spinach bowl", 
            "Roasted root vegetables with quinoa"
        ],
        "dinner": [
            "Brown rice with kidney bean curry", 
            "Stir-fried vegetables with buckwheat noodles", 
            "Lentil and mushroom shepherd's pie", 
            "Baked potatoes with black beans"
        ]
    },
    "Iron Deficiency": {
        "breakfast": [
            "Oatmeal with pumpkin seeds and raisins", 
            "Green smoothie with spinach and apple", 
            "Quinoa porridge with apricots", 
            "Buckwheat pancakes (egg-free) with berries"
        ],
        "lunch": [
            "Lentil and kale soup", 
            "Spinach salad with chickpeas and citrus dressing", 
            "White bean and tomato stew", 
            "Quinoa and roasted beet salad"
        ],
        "dinner": [
            "Lentil dahl with brown rice", 
            "Sauteed spinach with black eyed peas", 
            "Roasted Brussels sprouts with kidney beans", 
            "Vegetable and lentil shepherd's pie"
        ]
    },
    "Zinc Deficiency": {
        "breakfast": [
            "Oatmeal with pumpkin seeds", 
            "Quinoa porridge with hemp seeds", 
            "Chia seed pudding with berries", 
            "Millet bowl with sunflower seeds"
        ],
        "lunch": [
            "Chickpea and roasted vegetable salad", 
            "Lentil and spinach soup", 
            "Black bean bowl with avocado", 
            "Quinoa and roasted pumpkin salad"
        ],
        "dinner": [
            "Baked beans with baked potato", 
            "Lentil stew with carrots and celery", 
            "Stir-fried mixed beans with rice", 
            "Roasted root vegetables with chickpeas"
        ]
    },
    "Vitamin B3 Deficiency": {
        "breakfast": [
            "Oatmeal with sliced avocado", 
            "Brown rice porridge with green peas", 
            "Mushroom and spinach breakfast hash", 
            "Quinoa bowl with sauteed mushrooms"
        ],
        "lunch": [
            "Avocado and chickpea salad", 
            "Green pea and mint soup", 
            "Mushroom and lentil bowl", 
            "Roasted vegetable salad with ginger dressing"
        ],
        "dinner": [
            "Mushroom risotto (dairy-free)", 
            "Green pea and potato curry", 
            "Baked sweet potato with avocado and beans", 
            "Stir-fried mushrooms and broccoli with rice"
        ]
    },
    "Thyroid issues": {
        "breakfast": [
            "Oatmeal with mixed berries", 
            "Banana and spinach smoothie", 
            "Quinoa porridge with apple", 
            "Chia pudding with strawberries"
        ],
        "lunch": [
            "Broccoli and lentil soup", 
            "Spinach and strawberry salad", 
            "Roasted vegetable bowl with quinoa", 
            "Chickpea and broccoli salad"
        ],
        "dinner": [
            "Steamed broccoli with black beans", 
            "Spinach and potato curry", 
            "Baked root vegetables with lentils", 
            "Brown rice with mixed vegetable stir-fry"
        ]
    },
    "Vitamin D Deficiency": {
        "breakfast": [
            "Oatmeal with fortified plant milk", 
            "Mushroom and potato hash", 
            "Quinoa porridge with sliced bananas", 
            "Chia pudding made with fortified juice"
        ],
        "lunch": [
            "Mushroom and lentil soup", 
            "Roasted vegetable salad", 
            "Chickpea and spinach bowl", 
            "White bean and mushroom stew"
        ],
        "dinner": [
            "Sauteed mushrooms with brown rice", 
            "Lentil and vegetable dahl", 
            "Baked potato with roasted mushrooms", 
            "Mushroom risotto (dairy-free)"
        ]
    },
    "Low serum vitamin levels": {
        "breakfast": [
            "Oatmeal with mixed fruit", 
            "Quinoa bowl with berries", 
            "Green smoothie with spinach and apple", 
            "Millet porridge with banana"
        ],
        "lunch": [
            "Mixed bean salad with citrus dressing", 
            "Lentil and vegetable soup", 
            "Chickpea and roasted root vegetable bowl", 
            "Quinoa and spinach salad"
        ],
        "dinner": [
            "Brown rice with mixed bean curry", 
            "Stir-fried vegetables with buckwheat noodles", 
            "Lentil and mushroom stew", 
            "Baked sweet potato with mixed beans"
        ]
    },
    "Iodine Deficiency": {
        "breakfast": [
            "Oatmeal with apples and cinnamon", 
            "Green smoothie with spinach", 
            "Quinoa porridge with berries", 
            "Rice flakes with banana"
        ],
        "lunch": [
            "Seaweed and cucumber salad", 
            "Lentil soup with leafy greens", 
            "Roasted potato and bean bowl", 
            "Quinoa salad with mixed vegetables"
        ],
        "dinner": [
            "Brown rice with seaweed and vegetable stir-fry", 
            "Baked potatoes with leafy greens", 
            "Lentil and spinach curry", 
            "Roasted root vegetables with beans"
        ]
    },
    "Vitamin C Deficiency": {
        "breakfast": [
            "Oatmeal with strawberries", 
            "Citrus fruit salad", 
            "Green smoothie with orange juice", 
            "Quinoa bowl with kiwi"
        ],
        "lunch": [
            "Bell pepper and black bean salad", 
            "Broccoli and lentil soup", 
            "Citrus and spinach salad", 
            "Roasted tomato and bean bowl"
        ],
        "dinner": [
            "Stir-fried bell peppers and broccoli with rice", 
            "Tomato and lentil stew", 
            "Roasted Brussels sprouts with potatoes", 
            "Sweet potato and bell pepper curry"
        ]
    },
    "Vitamin E Deficiency": {
        "breakfast": [
            "Oatmeal with sunflower seeds", 
            "Green smoothie with spinach", 
            "Quinoa porridge with pumpkin seeds", 
            "Chia pudding with berries"
        ],
        "lunch": [
            "Spinach and avocado salad", 
            "Lentil soup with mixed greens", 
            "Roasted vegetable bowl", 
            "Chickpea salad with olive oil dressing"
        ],
        "dinner": [
            "Sauteed spinach with brown rice", 
            "Baked sweet potato with sunflower seeds", 
            "Lentil and vegetable dahl", 
            "Roasted root vegetables with olive oil"
        ]
    },
    "Omega-3 Deficiency": {
        "breakfast": [
            "Oatmeal with chia seeds", 
            "Flaxseed pudding with berries", 
            "Quinoa bowl with hemp seeds", 
            "Green smoothie with flaxseed oil"
        ],
        "lunch": [
            "Spinach salad with chia seeds", 
            "Lentil soup", 
            "Roasted vegetable bowl with hemp seeds", 
            "White bean and kale stew"
        ],
        "dinner": [
            "Brown rice with mixed bean curry", 
            "Baked sweet potato with flaxseeds", 
            "Lentil and vegetable stew", 
            "Stir-fried greens with rice"
        ]
    },
    "Vitamin B12 Deficiency": {
        "breakfast": [
            "Fortified oat cereal with plant milk", 
            "Smoothie with fortified juice", 
            "Quinoa porridge", 
            "Rice flakes with fruit"
        ],
        "lunch": [
            "Nutritional yeast and lentil soup", 
            "Black bean and corn salad", 
            "Chickpea bowl with roasted vegetables", 
            "Quinoa and spinach salad"
        ],
        "dinner": [
            "Brown rice with nutritional yeast sprinkled over beans", 
            "Lentil and mushroom stew", 
            "Baked potato with beans", 
            "Vegetable stir-fry with rice"
        ]
    },
    "No Vitamin Deficiency": {
        "breakfast": ["Balanced oatmeal with fruit"],
        "lunch": ["Mixed vegetable and bean salad"],
        "dinner": ["Balanced vegetable and rice bowl"]
    }
}
