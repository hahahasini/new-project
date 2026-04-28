import random
from app.config import FOOD_RECOMMENDATIONS


DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class DietPlannerService:
    """Generates weekly diet plans based on detected deficiency."""

    @staticmethod
    def generate_weekly_plan(deficiency: str) -> dict:
        """
        Generate a fixed weekly diet plan for the given deficiency.

        Args:
            deficiency: The detected vitamin deficiency string.

        Returns:
            Dict with 'weekly_plan' (list of day/meals dicts) and 'food_recommendations' (list of foods).
        """
        foods = FOOD_RECOMMENDATIONS.get(deficiency, {})

        if not foods:
            empty_meals = {"breakfast": ["No specific recommendation"], "lunch": ["No specific recommendation"], "dinner": ["No specific recommendation"]}
            return {
                "weekly_plan": [{"day": day, "meals": empty_meals} for day in DAYS],
                "food_recommendations": [],
            }

        weekly_plan = []
        for i, day in enumerate(DAYS):
            bfast = foods["breakfast"][i % len(foods["breakfast"])]
            lunch = foods["lunch"][i % len(foods["lunch"])]
            dinner = foods["dinner"][i % len(foods["dinner"])]
            
            weekly_plan.append({
                "day": day,
                "meals": {
                    "breakfast": [bfast],
                    "lunch": [lunch],
                    "dinner": [dinner]
                }
            })

        # Generate a flat list of recommendations from all meals
        flat_recommendations = []
        for meal_type in ["breakfast", "lunch", "dinner"]:
            for item in foods.get(meal_type, []):
                if item not in flat_recommendations:
                    flat_recommendations.append(item)

        return {
            "weekly_plan": weekly_plan,
            "food_recommendations": flat_recommendations,
        }
