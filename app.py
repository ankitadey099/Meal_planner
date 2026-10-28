import os
import random
import re
from collections import Counter

from flask import Flask, flash, redirect, render_template, request, session, url_for

# Move your big `meals = [...]` list into meals_data.py and rename it to MEALS.
from meals_data import MEALS as RAW_MEALS

app = Flask(__name__)
# Needed for session (per-user plan) and flash messages. Set a real one in production.
app.secret_key = os.environ.get("SECRET_KEY", "change-me-before-deploying")

# ------------------------------------------------------------------ constants
MEAL_TYPES = ["Breakfast", "Lunch", "Snack", "Dinner"]
CALORIE_SHARE = {"Breakfast": 0.25, "Lunch": 0.35, "Snack": 0.10, "Dinner": 0.30}
CALORIE_TOLERANCE = 100

ACTIVITY = {
    "sedentary": 1.2,      # little or no exercise
    "light": 1.375,        # 1-3 days/week
    "moderate": 1.55,      # 3-5 days/week
    "active": 1.725,       # 6-7 days/week
}
GOAL_ADJUST = {"weight_loss": -500, "maintain": 0, "muscle_gain": 300}

# What a person means by an allergy -> the ingredient words to block.
ALLERGEN_GROUPS = {
    "nuts": {"nuts", "almond", "cashew", "walnut", "peanut", "pistachio"},
    "dairy": {"milk", "paneer", "cheese", "cream", "yogurt", "curd", "ghee",
              "parmesan", "butter", "cottage cheese"},
    "gluten": {"wheat flour", "flour", "bread", "pasta", "semolina", "tortilla",
               "croutons", "breadcrumbs", "pita bread", "daliya", "crackers"},
    "egg": {"egg", "mayo", "mayonnaise"},
    "soy": {"soy sauce", "tofu", "edamame"},
    "fish": {"fish", "salmon", "tuna"},
    "shellfish": {"prawn", "shrimp"},
}
ALLERGY_ALIASES = {
    "nut": "nuts", "peanut": "nuts", "peanuts": "nuts", "almond": "nuts",
    "milk": "dairy", "lactose": "dairy", "wheat": "gluten",
    "eggs": "egg", "prawn": "shellfish", "prawns": "shellfish", "shrimp": "shellfish",
}
NON_VEGAN = ALLERGEN_GROUPS["dairy"] | {"egg", "honey", "mayo", "mayonnaise"}


# ------------------------------------------------------------------ data prep
def prepare_meals(raw):
    """Remove duplicate names and add a derived `vegan` flag to each meal."""
    seen, cleaned = set(), []
    for meal in raw:
        key = meal["name"].strip().lower()
        if key in seen:
            continue
        seen.add(key)
        meal = dict(meal)
        meal["vegan"] = meal["diet"] == "vegetarian" and not any(
            ingredient_hits(i, NON_VEGAN) for i in meal["ingredients"]
        )
        cleaned.append(meal)
    return cleaned


def ingredient_hits(ingredient, terms):
    """True if an ingredient contains any of the terms as a whole word."""
    ingredient = ingredient.lower()
    return any(re.search(rf"\b{re.escape(t)}s?\b", ingredient) for t in terms)


MEALS = prepare_meals(RAW_MEALS)
BY_NAME = {m["name"]: m for m in MEALS}


# ------------------------------------------------------------------ filtering
def expand_allergies(raw_text):
    """'nuts, Milk' -> every ingredient word that should be blocked."""
    terms = set()
    for item in raw_text.split(","):
        item = item.strip().lower()
        if not item:
            continue
        terms.add(item)
        terms |= ALLERGEN_GROUPS.get(ALLERGY_ALIASES.get(item, item), set())
    return terms


def is_eligible(meal, diet, blocked_terms, meal_type=None):
    """Hard rules: diet, meal type and allergies. These are never relaxed."""
    if meal_type and meal["meal_type"].lower() != meal_type.lower():
        return False
    if diet == "vegetarian" and meal["diet"] != "vegetarian":
        return False
    if diet == "vegan" and not meal["vegan"]:
        return False
    if blocked_terms and any(ingredient_hits(i, blocked_terms) for i in meal["ingredients"]):
        return False
    return True


def recommend(diet, blocked_terms, meal_type, calories, query):
    """Return (meals, notice). Fallbacks only choose from safe meals."""
    pool = [m for m in MEALS if is_eligible(m, diet, blocked_terms, meal_type)]

    if query:
        q = query.lower()
        pool = [m for m in pool
                if q in m["name"].lower() or any(q in i.lower() for i in m["ingredients"])]

    if not calories:
        return sorted(pool, key=lambda m: m["calories"]), None

    by_closeness = sorted(pool, key=lambda m: abs(m["calories"] - calories))
    close = [m for m in by_closeness if abs(m["calories"] - calories) <= CALORIE_TOLERANCE]
    if close:
        return close, None
    if by_closeness:
        return by_closeness[:3], (
            f"No meals within {CALORIE_TOLERANCE} kcal of {calories}. "
            "Showing the closest options that match your diet and allergies."
        )
    return [], "No meals match your diet, meal type and allergies. Try changing a filter."


def to_number(value, low, high, label):
    """Parse a form value; return (number, error)."""
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None, f"{label} must be a number."
    if not low <= number <= high:
        return None, f"{label} must be between {low:g} and {high:g}."
    return number, None


# ------------------------------------------------------------------ routes
@app.route("/", methods=["GET", "POST"])
def home():
    user_data, recommended_meals, notice = {}, [], None

    if request.method == "POST":
        diet = request.form.get("diet", "")
        meal_type = request.form.get("meal_type", "")
        query = request.form.get("q", "").strip()
        allergy_text = request.form.get("allergies", "")

        calories = 0
        raw_calories = request.form.get("calories", "").strip()
        if raw_calories:
            calories, error = to_number(raw_calories, 50, 3000, "Calories")
            if error:
                flash(error)
                calories = 0
            calories = int(calories or 0)

        user_data = {
            "diet": diet,
            "allergies": [a.strip().lower() for a in allergy_text.split(",") if a.strip()],
            "calories": calories,
            "meal_type": meal_type,
            "q": query,
        }
        recommended_meals, notice = recommend(
            diet, expand_allergies(allergy_text), meal_type, calories, query
        )

    return render_template(
        "dashboard.html",
        recommended_meals=recommended_meals,
        meals=MEALS,
        user_data=user_data,
        notice=notice,
    )


def calorie_target(sex, age, weight, height, activity, goal):
    """Mifflin-St Jeor BMR -> daily calories adjusted for the goal."""
    bmr = 10 * weight + 6.25 * height - 5 * age + (5 if sex == "male" else -161)
    tdee = bmr * ACTIVITY[activity]
    floor = 1500 if sex == "male" else 1200
    return round(max(tdee + GOAL_ADJUST[goal], floor)), round(bmr), round(tdee)


def pick_meal(pool, target, avoid):
    """Pick near the target calories, preferring meals not already used."""
    ranked = sorted(pool, key=lambda m: abs(m["calories"] - target))
    fresh = [m for m in ranked if m["name"] not in avoid]
    return random.choice((fresh or ranked)[:3])


def build_plan(prefs, daily_calories, days):
    blocked = expand_allergies(prefs["allergies"])
    pools = {mt: [m for m in MEALS if is_eligible(m, prefs["diet"], blocked, mt)]
             for mt in MEAL_TYPES}
    if any(not pool for pool in pools.values()):
        return None

    plan, used = [], set()
    for _ in range(days):
        day = {}
        for mt in MEAL_TYPES:
            choice = pick_meal(pools[mt], daily_calories * CALORIE_SHARE[mt], used)
            used.add(choice["name"])
            day[mt] = choice["name"]
        plan.append(day)
    return plan


def plan_context():
    """Everything plan.html needs, built from the session."""
    stored = session.get("plan")
    if not stored:
        return {"days": [], "grocery": []}

    days, grocery = [], Counter()
    for index, day in enumerate(stored["days"], start=1):
        meals = [{"type": mt, "meal": BY_NAME[day[mt]]} for mt in MEAL_TYPES if day[mt] in BY_NAME]
        for item in meals:
            grocery.update(i.lower() for i in item["meal"]["ingredients"])
        days.append({
            "label": f"Day {index}",
            "meals": meals,
            "totals": {k: sum(i["meal"][k] for i in meals)
                       for k in ("calories", "protein", "carbs", "fat")},
        })
    return {
        "days": days,
        "grocery": sorted(grocery.items()),
        "targets": stored["targets"],
    }


@app.route("/plan", methods=["GET", "POST"])
def plan():
    form = session.get("plan_form", {})

    if request.method == "POST":
        form = {k: request.form.get(k, "").strip() for k in
                ("sex", "age", "weight", "height", "activity", "goal", "diet", "allergies", "days")}
        session["plan_form"] = form

        age, e1 = to_number(form["age"], 14, 90, "Age")
        weight, e2 = to_number(form["weight"], 30, 250, "Weight (kg)")
        height, e3 = to_number(form["height"], 120, 230, "Height (cm)")
        errors = [e for e in (e1, e2, e3) if e]
        if form["sex"] not in ("male", "female") or form["activity"] not in ACTIVITY \
                or form["goal"] not in GOAL_ADJUST:
            errors.append("Choose sex, activity level and goal.")

        if errors:
            for error in errors:
                flash(error)
        else:
            daily, bmr, tdee = calorie_target(
                form["sex"], age, weight, height, form["activity"], form["goal"])
            days = 7 if form["days"] == "7" else 1
            days_plan = build_plan(form, daily, days)
            if days_plan is None:
                flash("Not enough meals match your diet and allergies to build a plan.")
            else:
                session["plan"] = {
                    "days": days_plan,
                    "targets": {"daily": daily, "bmr": bmr, "tdee": tdee},
                }
        return redirect(url_for("plan"))

    return render_template("plan.html", form=form, **plan_context())


@app.route("/plan/swap", methods=["POST"])
def swap():
    stored, form = session.get("plan"), session.get("plan_form")
    try:
        day_index = int(request.form.get("day", ""))
        meal_type = request.form.get("meal_type", "")
        day = stored["days"][day_index]
        current = day[meal_type]
    except (TypeError, ValueError, KeyError, IndexError):
        return redirect(url_for("plan"))

    blocked = expand_allergies(form["allergies"])
    pool = [m for m in MEALS
            if is_eligible(m, form["diet"], blocked, meal_type) and m["name"] != current]
    if pool:
        in_plan = {d[meal_type] for d in stored["days"]}
        target = stored["targets"]["daily"] * CALORIE_SHARE[meal_type]
        day[meal_type] = pick_meal(pool, target, in_plan)["name"]
        session["plan"] = stored
    else:
        flash("No other meal fits your diet and allergies for that slot.")
    return redirect(url_for("plan"))


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")
