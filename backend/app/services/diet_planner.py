import random
from app.config import FOOD_RECOMMENDATIONS


DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


class DietPlannerService:
    """Generates weekly diet plans based on detected deficiency."""

    @staticmethod
    def generate_weekly_plan(deficiency: str) -> dict:
        """
        Generate a weekly diet plan for the given deficiency.

        Args:
            deficiency: The detected vitamin deficiency string.

        Returns:
            Dict with 'weekly_plan' (list of day/foods dicts) and 'food_recommendations' (list of foods).
        """
        foods = FOOD_RECOMMENDATIONS.get(deficiency, [])

        if not foods:
            return {
                "weekly_plan": [{"day": day, "foods": ["No specific recommendation"]} for day in DAYS],
                "food_recommendations": [],
            }

        weekly_plan = []
        for day in DAYS:
            day_foods = random.sample(foods, min(3, len(foods)))
            weekly_plan.append({"day": day, "foods": day_foods})

        return {
            "weekly_plan": weekly_plan,
            "food_recommendations": foods,
        }
