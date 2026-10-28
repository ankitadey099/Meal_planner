# Meal Recommendation System

A Flask web app that recommends meals based on your diet, allergies and calorie needs, and builds a daily or weekly meal plan with a grocery list.

Built with Python (Flask), HTML and CSS.

## Features

- **Meal recommendations:** filter by diet (vegetarian, vegan, non-vegetarian), meal type, calories and allergies, or search by meal name or ingredient.
- **Allergy safety:** typing an allergy such as "nuts" or "dairy" also blocks related ingredients (almonds, peanut butter, paneer, cheese and so on). Fallback suggestions never include a blocked ingredient.
- **Calorie calculator:** estimates your daily calorie target from age, sex, weight, height, activity level and goal (lose weight, maintain, build muscle) using the Mifflin-St Jeor formula.
- **Meal planner:** creates a 1-day or 7-day plan with breakfast, lunch, snack and dinner, with calorie and macro totals for each day.
- **Swap meal:** replace any single meal in the plan with another one that fits your diet and allergies.
- **Grocery list:** combines the ingredients from the whole plan.
- **Input validation:** invalid numbers show a clear message instead of an error.

## Project structure

```
meal_app/
├── app.py              # Flask routes and recommendation logic
├── meals_data.py       # Meal dataset (list named MEALS)
├── requirements.txt    # Python dependencies
├── templates/
│   ├── dashboard.html  # Recommendation page
│   └── plan.html       # Meal plan page
└── static/             # CSS and other static files
```

## Getting started

**Requirements:** Python 3.9 or newer.

1. Clone or download the project and open a terminal in its folder.

2. (Optional) Create a virtual environment:

   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS / Linux
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:

   ```bash
   python app.py
   ```

5. Open <http://127.0.0.1:5000> in your browser. The meal planner is at `/plan`.

## How it works

1. **Hard rules first.** Diet, meal type and allergies are always applied and are never relaxed.
2. **Calories second.** Meals within 100 kcal of your target are shown, closest first. If none match, the three closest safe meals are shown with a notice.
3. **Planning.** Your daily target is split across meals (breakfast 25%, lunch 35%, snack 10%, dinner 30%). For each slot, the app picks one of the three closest-matching meals and avoids repeats where possible.
4. **Per-user data.** Your plan is stored in your browser session, so different visitors never see each other's plans.

## Configuration

| Variable | Purpose | Default |
| --- | --- | --- |
| `SECRET_KEY` | Signs the session cookie. Set your own value before deploying. | development placeholder |
| `FLASK_DEBUG` | Set to `1` to turn on debug mode. | off |

## Limitations

- Calorie targets are estimates for general guidance and are not medical or dietary advice. People with medical conditions or serious allergies should consult a doctor or dietitian.
- Allergy matching works on ingredient names in the dataset, so always check real food labels.
- Nutrition values in the dataset are approximate.

## Future improvements

- Save favorite meals
- Nutrition charts
- Download the plan as PDF
- Move the dataset to SQLite
- User accounts

## Author

Ankita Dey
