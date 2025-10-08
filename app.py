
from flask import Flask, render_template, request,redirect,url_for
import json
import os
app = Flask(__name__)

DATA_FILE ="user_data.json"
# Helper function to load data
# Example meal dataset
meals = [
    {"name": "Oats with Milk", "meal_type": "Breakfast", "calories": 300, "protein": 25, "carbs": 40, "fat": 8,
     "diet": "vegetarian", "ingredients": ["oats", "milk"],
     "image_url":"https://www.mississippivegan.com/wp-content/uploads/2024/08/bananas-and-cream-oatmeal-05-819x1024.jpg"},
    {"name": "Grilled Chicken Salad", "meal_type": "Lunch", "calories": 350, "protein": 30, "carbs": 15, "fat": 12,
     "diet": "non-vegetarian", "ingredients": ["chicken", "lettuce", "tomato"],
     "image_url":"https://www.eatingbirdfood.com/wp-content/uploads/2023/06/grilled-chicken-salad-hero.jpg"},
    {"name": "Paneer Wrap", "meal_type": "Dinner", "calories": 400, "protein": 28, "carbs": 35, "fat": 15,
     "diet": "vegetarian", "ingredients": ["paneer", "tortilla", "capsicum"],
     "image_url":"https://cdn.uengage.io/uploads/18085/image-646359-1717590397.jpeg"},
    {"name": "Protein Smoothie", "meal_type": "Snack", "calories": 200, "protein": 20, "carbs": 18, "fat": 5,
     "diet": "vegetarian", "ingredients": ["banana", "milk", "protein powder"],
     "image_url":"https://ichef.bbci.co.uk/food/ic/food_16x9_1600/recipes/protein_shake_21728_16x9.jpg"},
    {"name": "Egg Omelette", "meal_type": "Breakfast", "calories": 250, "protein": 22, "carbs": 5, "fat": 18,
     "diet": "non-vegetarian", "ingredients": ["eggs", "onion", "oil"],
     "image_url":"https://www.simplyquinoa.com/wp-content/uploads/2023/03/egg-white-omelet-1.jpg"},
    {
        "name": "Oatmeal with Berries",
        "meal_type": "Breakfast",
        "diet": "vegetarian",
        "calories": 320,
        "protein": 12,
        "carbs": 55,
        "fat": 8,
        "ingredients": ["oats", "milk", "berries", "honey"],
        "image_url":"https://d2t88cihvgacbj.cloudfront.net/manage/wp-content/uploads/2016/02/Triple-Berry-Oatmeal-Breakfast-Bowl-3.jpg?x19264"
    },
    {
        "name": "Scrambled Eggs with Spinach",
        "meal_type": "Breakfast",
        "diet": "non-vegetarian",
        "calories": 280,
        "protein": 18,
        "carbs": 5,
        "fat": 20,
        "ingredients": ["eggs", "spinach", "olive oil", "salt"],
        "image_url":"https://www.platingsandpairings.com/wp-content/uploads/2023/03/spinach-scrambled-eggs-recipe-8-scaled.jpg"
    },

    {
        "name": "Paneer Tikka Bowl",
        "meal_type": "Lunch",
        "diet": "vegetarian",
        "calories": 420,
        "protein": 28,
        "carbs": 30,
        "fat": 18,
        "ingredients": ["paneer", "bell pepper", "onion", "spices"],
        "image_url":"https://naturallynidhi.com/wp-content/uploads/2020/04/TandooriPaneerBowl_Cover.jpg"
    },
    {
        "name": "Veggie Stir Fry with Rice",
        "meal_type": "Dinner",
        "diet": "vegetarian",
        "calories": 500,
        "protein": 16,
        "carbs": 80,
        "fat": 12,
        "ingredients": ["rice", "broccoli", "carrot", "soy sauce", "tofu"],
        "image_url":"https://cookingwithcoit.com/wp-content/uploads/2021/04/CARD_Vegetable-Stir-Fry.jpg"
    },
    {
        "name": "Fish Curry with Brown Rice",
        "meal_type": "Dinner",
        "diet": "non-vegetarian",
        "calories": 550,
        "protein": 32,
        "carbs": 60,
        "fat": 20,
        "ingredients": ["fish", "curry sauce", "brown rice", "spices"],
        "image_url":"https://vaya.in/recipes/wp-content/uploads/2018/06/Meen-Alleppey-Curry-with-Brown-Rice.jpg"
    },
    {
        "name": "Fruit & Nut Smoothie",
        "meal_type": "Snack",
        "diet": "vegetarian",
        "calories": 250,
        "protein": 10,
        "carbs": 35,
        "fat": 8,
        "ingredients": ["banana", "milk", "almonds", "peanut butter"],
        "image_url":"https://lifesmoothies.ae/wp-content/uploads/2022/10/LS_Destacada-9-1.jpg"
    },
    {
        "name": "Boiled Eggs & Apple",
        "meal_type": "Snack",
        "diet": "non-vegetarian",
        "calories": 200,
        "protein": 14,
        "carbs": 18,
        "fat": 9,
        "ingredients": ["eggs", "apple"],
        "image_url":"https://i.pinimg.com/736x/b8/c9/c0/b8c9c0d4f2a18695c5b88606d1114570.jpg"
    },
{
        "name": "Poha with Vegetables",
        "meal_type": "Breakfast",
        "diet": "vegetarian",
        "calories": 300,
        "protein": 8,
        "carbs": 60,
        "fat": 6,
        "ingredients": ["flattened rice", "onion", "peas", "carrot", "spices"],
        "image_url":"https://www.mrishtanna.com/wp-content/uploads/2018/04/poha-indian-breakfast-recipe.jpg"
    },
{
        "name": "Idli with Sambar",
        "meal_type": "Breakfast",
        "diet": "vegetarian",
        "calories": 350,
        "protein": 10,
        "carbs": 65,
        "fat": 5,
        "ingredients": ["idli", "lentils", "vegetables", "tamarind"],
        "image_url":"https://shwetainthekitchen.com/wp-content/uploads/2022/01/Idli-Sambar.jpg"
    },
    {
        "name": "Avocado Toast with Egg",
        "meal_type": "Breakfast",
        "diet": "non-vegetarian",
        "calories": 370,
        "protein": 15,
        "carbs": 40,
        "fat": 18,
        "ingredients": ["bread", "avocado", "egg", "salt", "pepper"],
        "image_url":"https://www.aberdeenskitchen.com/wp-content/uploads/2019/05/Avocado-Egg-Breakfast-Toast-FI-Thumbnail-1200X1200.jpg"
    },
{
        "name": "Rajma Chawal",
        "meal_type": "Lunch",
        "diet": "vegetarian",
        "calories": 480,
        "protein": 18,
        "carbs": 85,
        "fat": 9,
        "ingredients": ["kidney beans", "rice", "onion", "tomato", "spices"],
        "image_url":"https://www.secondrecipe.com/wp-content/uploads/2017/08/rajma-chawal-1-500x500.jpg"
    },
# --- BREAKFAST ---
{
    "name": "Vegetable Upma",
    "meal_type": "Breakfast",
    "diet": "vegetarian",
    "calories": 310,
    "protein": 9,
    "carbs": 55,
    "fat": 7,
    "ingredients": ["semolina", "carrot", "peas", "beans", "spices"],
    "image_url":"https://cdn.cdnparenting.com/articles/2020/03/03172331/VEG-UPMA.webp"
},
{
    "name": "Masala Dosa with Coconut Chutney",
    "meal_type": "Breakfast",
    "diet": "vegetarian",
    "calories": 380,
    "protein": 9,
    "carbs": 65,
    "fat": 12,
    "ingredients": ["rice", "urad dal", "potato", "onion", "coconut"],
    "image_url":"https://www.vegrecipesofindia.com/wp-content/uploads/2021/06/coconut-chutney-1.jpg"
},
{
    "name": "Paratha with Curd",
    "meal_type": "Breakfast",
    "diet": "vegetarian",
    "calories": 420,
    "protein": 12,
    "carbs": 60,
    "fat": 14,
    "ingredients": ["wheat flour", "potato", "curd", "spices"],
    "image_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiRAYB4jp-MLEMEqSEZDOXQQZ5_qtcsq5O_Q&s"
},
{
    "name": "Moong Dal Chilla",
    "meal_type": "Breakfast",
    "diet": "vegetarian",
    "calories": 280,
    "protein": 14,
    "carbs": 35,
    "fat": 8,
    "ingredients": ["moong dal", "onion", "tomato", "spices"],
    "image_url":"https://www.vegrecipesofindia.com/wp-content/uploads/2016/11/moong-dal-chilla-3u.jpg"
},
{
    "name": "Egg Omelette with Toast",
    "meal_type": "Breakfast",
    "diet": "non-vegetarian",
    "calories": 330,
    "protein": 18,
    "carbs": 25,
    "fat": 16,
    "ingredients": ["eggs", "bread", "onion", "tomato", "spices"],
    "image_url":"https://recipesblob.oetker.in/assets/bed50b6fbbb84fc0ae786136d5351af4/750x910/bread-omelette.jpg"
},
{
    "name": "Banana Pancakes",
    "meal_type": "Breakfast",
    "diet": "vegetarian",
    "calories": 360,
    "protein": 10,
    "carbs": 58,
    "fat": 10,
    "ingredients": ["banana", "flour", "milk", "egg", "honey"],
    "image_url":"https://rainbowplantlife.com/wp-content/uploads/2025/05/Banana-pancakes-cover-photo.jpg"
},
{
    "name": "Smoothie Bowl",
    "meal_type": "Breakfast",
    "diet": "vegetarian",
    "calories": 290,
    "protein": 11,
    "carbs": 45,
    "fat": 9,
    "ingredients": ["banana", "berries", "yogurt", "granola"],
    "image_url":"https://www.superhealthykids.com/wp-content/uploads/2019/12/Mango-Smoothie-Bowl-1.jpeg"
},
{
    "name": "Avocado Toast with Tomato",
    "meal_type": "Breakfast",
    "diet": "vegetarian",
    "calories": 310,
    "protein": 9,
    "carbs": 40,
    "fat": 14,
    "ingredients": ["bread", "avocado", "tomato", "lemon"],
    "image_url":"https://www.veggiessavetheday.com/wp-content/uploads/2021/09/Tomato-Avocado-Toast-FI-1200x1200-1.jpg"
},
{
    "name": "Boiled Eggs with Whole Wheat Bread",
    "meal_type": "Breakfast",
    "diet": "non-vegetarian",
    "calories": 270,
    "protein": 16,
    "carbs": 28,
    "fat": 9,
    "ingredients": ["eggs", "bread", "butter"],
    "image_url":"https://d18zdz9g6n5za7.cloudfront.net/blog/1075-quick-egg-salad-af06.jpg"
},
{
    "name": "Cornflakes with Milk & Fruits",
    "meal_type": "Breakfast",
    "diet": "vegetarian",
    "calories": 280,
    "protein": 8,
    "carbs": 52,
    "fat": 4,
    "ingredients": ["cornflakes", "milk", "banana", "apple"],
    "image_url":"https://as2.ftcdn.net/jpg/02/09/54/11/1000_F_209541147_EeuElTsWuQBH7IbNEEOrb0BqMGqsfI4k.jpg"
},
{
    "name": "Aloo Puri",
    "meal_type": "Breakfast",
    "diet": "vegetarian",
    "calories": 450,
    "protein": 10,
    "carbs": 70,
    "fat": 15,
    "ingredients": ["wheat flour", "potato", "spices", "oil"],
    "image_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTEz_zx3PcGpLcMEsDvqeRkDzTvQ3_nvxGR7A&s"
},
{
    "name": "Thepla with Pickle",
    "meal_type": "Breakfast",
    "diet": "vegetarian",
    "calories": 330,
    "protein": 9,
    "carbs": 50,
    "fat": 11,
    "ingredients": ["wheat flour", "fenugreek leaves", "spices", "oil"],
    "image_url":"https://www.indianhealthyrecipes.com/wp-content/uploads/2023/03/thepla-recipe.webp"
},
{
    "name": "Sabudana Khichdi",
    "meal_type": "Breakfast",
    "diet": "vegetarian",
    "calories": 380,
    "protein": 7,
    "carbs": 65,
    "fat": 12,
    "ingredients": ["sago", "peanuts", "potato", "spices"],
    "image_url":"https://j6e2i8c9.delivery.rocketcdn.me/wp-content/uploads/2018/03/Sabudana-Khichdi-Recipe-2.jpg"
},
{
    "name": "Vegetable Sandwich",
    "meal_type": "Breakfast",
    "diet": "vegetarian",
    "calories": 320,
    "protein": 8,
    "carbs": 45,
    "fat": 10,
    "ingredients": ["bread", "cucumber", "tomato", "capsicum", "mint chutney"],
    "image_url":"https://www.themediterraneandish.com/wp-content/uploads/2024/03/Vegetable-Sandwich-Cropped-1.jpg"
},
{
    "name": "Egg Bhurji with Roti",
    "meal_type": "Breakfast",
    "diet": "non-vegetarian",
    "calories": 390,
    "protein": 22,
    "carbs": 35,
    "fat": 15,
    "ingredients": ["eggs", "onion", "tomato", "roti", "spices"],
    "image_url":"https://i.pinimg.com/564x/03/69/13/03691338e986db3608ac0d2e0a773ec0.jpg"
},
{
    "name": "Pesarattu (Green Gram Dosa)",
    "meal_type": "Breakfast",
    "diet": "vegetarian",
    "calories": 340,
    "protein": 15,
    "carbs": 55,
    "fat": 7,
    "ingredients": ["green gram", "ginger", "onion", "spices"],
    "image_url":"https://i0.wp.com/www.chitrasfoodbook.com/wp-content/uploads/2022/07/pesarattu-allam-pachadi-1.jpg?ssl=1"
},
{
    "name": "Rava Kesari with Milk",
    "meal_type": "Breakfast",
    "diet": "vegetarian",
    "calories": 360,
    "protein": 6,
    "carbs": 60,
    "fat": 12,
    "ingredients": ["semolina", "milk", "sugar", "ghee", "cardamom"],
    "image_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-QKiaoZlL9oGelSAlADlskA_0_yVd8ROh6Q&s"
},
{
    "name": "Peanut Butter Toast with Banana",
    "meal_type": "Breakfast",
    "diet": "vegetarian",
    "calories": 310,
    "protein": 12,
    "carbs": 38,
    "fat": 14,
    "ingredients": ["bread", "peanut butter", "banana"],
    "image_url":"https://40aprons.com/wp-content/uploads/2014/03/peanut-butter-banana-toast-1-1.jpg"
},
{
    "name": "Protein Shake with Oats",
    "meal_type": "Breakfast",
    "diet": "vegetarian",
    "calories": 350,
    "protein": 28,
    "carbs": 30,
    "fat": 10,
    "ingredients": ["protein powder", "milk", "oats", "banana"],
    "image_url":"https://www.eatingbirdfood.com/wp-content/uploads/2022/02/oatmeal-smoothie-hero.jpg"
},
{
    "name": "Vegetable Daliya (Broken Wheat Porridge)",
    "meal_type": "Breakfast",
    "diet": "vegetarian",
    "calories": 300,
    "protein": 10,
    "carbs": 55,
    "fat": 6,
    "ingredients": ["daliya", "carrot", "peas", "beans", "spices"],
    "image_url":"https://j6e2i8c9.delivery.rocketcdn.me/wp-content/uploads/2018/09/Instant-Pot-vegetable-daliya-recipe-05.jpg.webp"
},
# --- LUNCH ---
{
    "name": "Chole with Rice",
    "meal_type": "Lunch",
    "diet": "vegetarian",
    "calories": 500,
    "protein": 18,
    "carbs": 80,
    "fat": 12,
    "ingredients": ["chickpeas", "rice", "onion", "tomato", "spices"],
    "image_url":"https://images.immediate.co.uk/production/volatile/sites/30/2021/02/Chole-with-cumin-rice-and-raita-b00cba7.jpg"
},
{
    "name": "Grilled Chicken Sandwich",
    "meal_type": "Lunch",
    "diet": "non-vegetarian",
    "calories": 420,
    "protein": 32,
    "carbs": 35,
    "fat": 15,
    "ingredients": ["bread", "chicken", "lettuce", "tomato", "mayo"],
    "image_url":"https://easychickenrecipes.com/wp-content/uploads/2023/06/grilled-chicken-sandwich-1-of-6-edited.jpg"
},
{
    "name": "Vegetable Quinoa Bowl",
    "meal_type": "Lunch",
    "diet": "vegetarian",
    "calories": 450,
    "protein": 15,
    "carbs": 60,
    "fat": 12,
    "ingredients": ["quinoa", "broccoli", "carrot", "beans", "olive oil"],
    "image_url":"https://www.emilieeats.com/wp-content/uploads/2016/09/greek-quinoa-buddha-bowl-vegan-gluten-free-1.jpg"
},
{
    "name": "Fish Tacos",
    "meal_type": "Lunch",
    "diet": "non-vegetarian",
    "calories": 480,
    "protein": 28,
    "carbs": 50,
    "fat": 16,
    "ingredients": ["fish", "tortilla", "lettuce", "tomato", "salsa"],
    "image_url":"https://natashaskitchen.com/wp-content/uploads/2017/08/Easy-Fish-Tacos-with-the-Best-Fish-Taco-Sauce-4.jpg"
},
{
    "name": "Rajma with Roti",
    "meal_type": "Lunch",
    "diet": "vegetarian",
    "calories": 460,
    "protein": 17,
    "carbs": 70,
    "fat": 10,
    "ingredients": ["kidney beans", "wheat flour", "onion", "tomato", "spices"],
    "image_url":"https://d34vm3j4h7f97z.cloudfront.net/original/3X/4/b/4be7a6303754ae2ea91eaed644900f4141c40c92.jpeg"
},
{
    "name": "Chicken Caesar Salad",
    "meal_type": "Lunch",
    "diet": "non-vegetarian",
    "calories": 400,
    "protein": 30,
    "carbs": 20,
    "fat": 18,
    "ingredients": ["chicken", "lettuce", "parmesan", "croutons", "caesar dressing"],
    "image_url":"https://www.gimmesomeoven.com/wp-content/uploads/2015/08/Caesar-Pasta-Salad-Recipe-9.jpg"
},
{
    "name": "Vegetable Pasta",
    "meal_type": "Lunch",
    "diet": "vegetarian",
    "calories": 430,
    "protein": 14,
    "carbs": 65,
    "fat": 12,
    "ingredients": ["pasta", "tomato sauce", "zucchini", "bell pepper", "olive oil"],
    "image_url":"https://www.cubesnjuliennes.com/wp-content/uploads/2023/11/Vegetable-Pasta-Recipe.jpg"
},
{
    "name": "Egg Fried Rice",
    "meal_type": "Lunch",
    "diet": "non-vegetarian",
    "calories": 500,
    "protein": 22,
    "carbs": 65,
    "fat": 18,
    "ingredients": ["rice", "egg", "peas", "carrot", "soy sauce"],
    "image_url":"https://www.indianhealthyrecipes.com/wp-content/uploads/2021/07/egg-fried-rice-recipe.jpg"
},
{
    "name": "Palak Paneer with Rice",
    "meal_type": "Lunch",
    "diet": "vegetarian",
    "calories": 480,
    "protein": 22,
    "carbs": 55,
    "fat": 18,
    "ingredients": ["spinach", "paneer", "rice", "spices"],
    "image_url":"https://veganbell.com/wp-content/uploads/2021/03/Palak-Paneer-scaled.jpg"
},
{
    "name": "Grilled Fish with Veggies",
    "meal_type": "Lunch",
    "diet": "non-vegetarian",
    "calories": 520,
    "protein": 35,
    "carbs": 30,
    "fat": 20,
    "ingredients": ["fish", "broccoli", "carrot", "olive oil", "lemon"],
    "image_url":"https://img.taste.com.au/ykyHrKeZ/taste/2016/11/grilled-vegetables-and-snapper-86243-1.jpeg"
},
# --- LUNCH ---
{
    "name": "Methi Thepla with Yogurt",
    "meal_type": "Lunch",
    "diet": "vegetarian",
    "calories": 400,
    "protein": 12,
    "carbs": 60,
    "fat": 14,
    "ingredients": ["wheat flour", "fenugreek leaves", "spices", "oil", "yogurt"],
    "image_url":"https://ministryofcurry.com/wp-content/uploads/2022/04/methi-thepla.jpg"
},
{
    "name": "Tandoori Chicken with Salad",
    "meal_type": "Lunch",
    "diet": "non-vegetarian",
    "calories": 500,
    "protein": 40,
    "carbs": 20,
    "fat": 22,
    "ingredients": ["chicken", "yogurt", "spices", "lettuce", "tomato"],
    "image_url":"https://www.licious.in/blog/wp-content/uploads/2022/03/shutterstock_1089760742-min.jpg"
},
{
    "name": "Mixed Vegetable Pulao",
    "meal_type": "Lunch",
    "diet": "vegetarian",
    "calories": 450,
    "protein": 14,
    "carbs": 70,
    "fat": 12,
    "ingredients": ["rice", "peas", "carrot", "beans", "spices"],
    "image_url":"https://www.indianveggiedelight.com/wp-content/uploads/2019/07/veg-pulao-featured.jpg"
},
{
    "name": "Butter Chicken with Rice",
    "meal_type": "Lunch",
    "diet": "non-vegetarian",
    "calories": 600,
    "protein": 35,
    "carbs": 60,
    "fat": 25,
    "ingredients": ["chicken", "butter", "cream", "rice", "spices"],
    "image_url":"https://thefoodieglobetrotter.com/wp-content/uploads/2020/05/Takeout-Kit-Indian-Butter-Chicken-Tikka-Masala-Basmati-Rice-Meal-Kit.jpg"
},
{
    "name": "Vegetable Wrap",
    "meal_type": "Lunch",
    "diet": "vegetarian",
    "calories": 370,
    "protein": 10,
    "carbs": 50,
    "fat": 15,
    "ingredients": ["tortilla", "lettuce", "carrot", "capsicum", "hummus"],
    "image_url":"https://kristineskitchenblog.com/wp-content/uploads/2024/04/veggie-wrap-11-2.jpg"
},
{
    "name": "Grilled Turkey Sandwich",
    "meal_type": "Lunch",
    "diet": "non-vegetarian",
    "calories": 420,
    "protein": 30,
    "carbs": 35,
    "fat": 15,
    "ingredients": ["bread", "turkey", "lettuce", "tomato", "mayo"],
    "image_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTxLXCmb1L3sELwv2r4KGGG49xeSl0N-7qYJQ&s"
},
{
    "name": "Stuffed Capsicum with Paneer",
    "meal_type": "Lunch",
    "diet": "vegetarian",
    "calories": 430,
    "protein": 20,
    "carbs": 40,
    "fat": 18,
    "ingredients": ["capsicum", "paneer", "onion", "spices"],
    "image_url":"https://vegecravings.com/wp-content/uploads/2017/03/stuffed-capsicum-recipe-step-by-step-instructions.jpg"
},
{
    "name": "Egg Curry with Roti",
    "meal_type": "Lunch",
    "diet": "non-vegetarian",
    "calories": 480,
    "protein": 25,
    "carbs": 45,
    "fat": 20,
    "ingredients": ["eggs", "onion", "tomato", "spices", "roti"],
    "image_url":"https://www.poultryrecipes.co.in/media/cache/egg-curry-recipe_608x385.jpg"
},
{
    "name": "Lentil Soup with Bread",
    "meal_type": "Lunch",
    "diet": "vegetarian",
    "calories": 350,
    "protein": 16,
    "carbs": 50,
    "fat": 8,
    "ingredients": ["lentils", "carrot", "celery", "bread", "spices"],
    "image_url":"https://www.jocooks.com/wp-content/uploads/2020/04/lentil-soup-1-17.jpg"
},
{
    "name": "Chicken Burrito Bowl",
    "meal_type": "Lunch",
    "diet": "non-vegetarian",
    "calories": 520,
    "protein": 38,
    "carbs": 55,
    "fat": 18,
    "ingredients": ["chicken", "rice", "beans", "lettuce", "salsa"],
    "image_url":"https://www.simplysissom.com/wp-content/uploads/2019/07/Healthy-Burrito-Bowls-With-Cilantro-Lime-Dressing-FI-1.jpg"
},
# --- LUNCH ---
{
    "name": "Vegetable Biryani",
    "meal_type": "Lunch",
    "diet": "vegetarian",
    "calories": 480,
    "protein": 14,
    "carbs": 75,
    "fat": 15,
    "ingredients": ["rice", "carrot", "peas", "beans", "spices", "yogurt"],
    "image_url":"https://www.madhuseverydayindian.com/wp-content/uploads/2022/11/easy-vegetable-biryani.jpg"
},
{
    "name": "Grilled Salmon with Quinoa",
    "meal_type": "Lunch",
    "diet": "non-vegetarian",
    "calories": 520,
    "protein": 38,
    "carbs": 35,
    "fat": 20,
    "ingredients": ["salmon", "quinoa", "spinach", "lemon", "olive oil"],
    "image_url":"https://www.eatingwell.com/thmb/RT-ah2NSs9DNZMAtrdWeju7JmfQ=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/7493350-be9d56bbbaf6461aa9f503b8e94462de.jpg"
},
{
    "name": "Stuffed Paratha with Yogurt",
    "meal_type": "Lunch",
    "diet": "vegetarian",
    "calories": 450,
    "protein": 12,
    "carbs": 60,
    "fat": 18,
    "ingredients": ["wheat flour", "potato", "paneer", "spices", "yogurt"],
    "image_url":"https://static.wixstatic.com/media/26b5bf_d114351e1fb447e3a040bf1555a70c0a~mv2.jpg/v1/fill/w_980,h_1351,al_c,q_85,usm_0.66_1.00_0.01,enc_avif,quality_auto/26b5bf_d114351e1fb447e3a040bf1555a70c0a~mv2.jpg"
},
{
    "name": "Chicken Shawarma Wrap",
    "meal_type": "Lunch",
    "diet": "non-vegetarian",
    "calories": 480,
    "protein": 32,
    "carbs": 45,
    "fat": 18,
    "ingredients": ["chicken", "tortilla", "lettuce", "tomato", "yogurt sauce"],
    "image_url":"https://gimmedelicious.com/wp-content/uploads/2024/03/Chicken-Shawarma-Wraps-sq.jpg"
},
{
    "name": "Vegetable Lentil Salad",
    "meal_type": "Lunch",
    "diet": "vegetarian",
    "calories": 350,
    "protein": 15,
    "carbs": 40,
    "fat": 12,
    "ingredients": ["lentils", "cucumber", "tomato", "onion", "olive oil"],
    "image_url":"https://www.twopeasandtheirpod.com/wp-content/uploads/2025/01/Roasted-Vegetable-Lentil-Salad-4548.jpg"
},
{
    "name": "Turkey & Avocado Sandwich",
    "meal_type": "Lunch",
    "diet": "non-vegetarian",
    "calories": 420,
    "protein": 30,
    "carbs": 35,
    "fat": 15,
    "ingredients": ["bread", "turkey", "avocado", "lettuce", "tomato"],
    "image_url":"https://i0.wp.com/wanderingchickpea.com/wp-content/uploads/2023/08/Honey-mustard-turkey-avocado-sandwich-5.jpg?resize=540%2C720&ssl=1"
},
{
    "name": "Mushroom Risotto",
    "meal_type": "Lunch",
    "diet": "vegetarian",
    "calories": 470,
    "protein": 14,
    "carbs": 65,
    "fat": 18,
    "ingredients": ["rice", "mushroom", "parmesan", "olive oil", "onion"],
    "image_url":"https://static01.nyt.com/images/2024/01/10/multimedia/10Risotto-gcmz/10Risotto-gcmz-mediumSquareAt3X.jpg"
},
{
    "name": "Egg Salad Sandwich",
    "meal_type": "Lunch",
    "diet": "non-vegetarian",
    "calories": 400,
    "protein": 22,
    "carbs": 35,
    "fat": 15,
    "ingredients": ["bread", "eggs", "lettuce", "tomato", "mayonnaise"],
    "image_url":"https://www.thegraciouswife.com/wp-content/uploads/2022/04/Classic-Egg-Salad-featurex.jpg"
},
{
    "name": "Chickpea & Spinach Curry with Rice",
    "meal_type": "Lunch",
    "diet": "vegetarian",
    "calories": 450,
    "protein": 18,
    "carbs": 65,
    "fat": 12,
    "ingredients": ["chickpeas", "spinach", "rice", "onion", "spices"],
    "image_url":"https://vancouverwithlove.com/wp-content/uploads/2024/08/chickpea-spinach-curry-2.jpg"
},
{
    "name": "Grilled Prawn Salad",
    "meal_type": "Lunch",
    "diet": "non-vegetarian",
    "calories": 480,
    "protein": 36,
    "carbs": 25,
    "fat": 18,
    "ingredients": ["prawns", "lettuce", "cucumber", "tomato", "olive oil"],
    "image_url":"https://healthyfitnessmeals.com/wp-content/uploads/2022/07/Grilled-Shrimp-salad-6.jpg"
},
# ---------- DINNER ----------
{"name": "Veggie Stir Fry with Rice", "meal_type": "Dinner", "diet": "vegetarian", "calories": 500, "protein": 16, "carbs": 80, "fat": 12, "ingredients": ["rice","broccoli","carrot","soy sauce","tofu"],"image_url":"https://cookingwithcoit.com/wp-content/uploads/2021/04/CARD_Vegetable-Stir-Fry.jpg"},
{"name": "Chicken Biryani", "meal_type": "Dinner", "diet": "non-vegetarian", "calories": 600, "protein": 30, "carbs": 75, "fat": 22, "ingredients": ["chicken","rice","spices","yogurt"],"image_url":"https://j6e2i8c9.delivery.rocketcdn.me/wp-content/uploads/2020/09/Chicken-Biryani-Recipe-01-1-500x500.jpg"},
{"name": "Palak Paneer with Roti", "meal_type": "Dinner", "diet": "vegetarian", "calories": 480, "protein": 22, "carbs": 45, "fat": 18, "ingredients": ["spinach","paneer","wheat flour","spices"],"image_url":"https://i.pinimg.com/736x/2e/62/6b/2e626bbc7d017763cc818de928717735.jpg"},
{"name": "Grilled Salmon with Vegetables", "meal_type": "Dinner", "diet": "non-vegetarian", "calories": 520, "protein": 35, "carbs": 25, "fat": 22, "ingredients": ["salmon","broccoli","zucchini","lemon"],"image_url":"https://hungryfoodie.com/wp-content/uploads/2023/09/Sheet-Pan-Salmon-and-Vegetables-21.jpg"},
{"name": "Stuffed Bell Peppers", "meal_type": "Dinner", "diet": "vegetarian", "calories": 450, "protein": 18, "carbs": 55, "fat": 15, "ingredients": ["bell pepper","rice","beans","cheese","spices"],"image_url":"https://tyberrymuch.com/wp-content/uploads/2020/09/vegan-stuffed-peppers-recipe-720x720.jpg"},
{"name": "Mushroom Risotto", "meal_type": "Dinner", "diet": "vegetarian", "calories": 470, "protein": 14, "carbs": 70, "fat": 16, "ingredients": ["rice","mushrooms","cream","cheese","onion"],"image_url":"https://static01.nyt.com/images/2024/01/10/multimedia/10Risotto-gcmz/10Risotto-gcmz-mediumSquareAt3X.jpg"},
{"name": "Grilled Chicken with Quinoa", "meal_type": "Dinner", "diet": "non-vegetarian", "calories": 540, "protein": 38, "carbs": 50, "fat": 20, "ingredients": ["chicken","quinoa","broccoli","olive oil"],"image_url":"https://mealpractice.b-cdn.net/141821845962887168/grilled-lemon-herb-chicken-with-roasted-vegetables-and-quinoa-bnoJdKRkho.webp"},
{"name": "Eggplant Parmesan", "meal_type": "Dinner", "diet": "vegetarian", "calories": 490, "protein": 20, "carbs": 60, "fat": 18, "ingredients": ["eggplant","tomato","cheese","breadcrumbs"],"image_url":"https://www.honeywhatscooking.com/wp-content/uploads/2023/09/eggplant-parmesan-pasta-featured2-1.jpg"},
{"name": "Shrimp Stir Fry", "meal_type": "Dinner", "diet": "non-vegetarian", "calories": 480, "protein": 32, "carbs": 40, "fat": 16, "ingredients": ["shrimp","bell pepper","soy sauce","garlic"],"image_url":"https://healthyrecipesblogs.com/wp-content/uploads/2024/12/shrimp-stir-fry-featured-new.jpg"},
{"name": "Paneer Butter Masala with Rice", "meal_type": "Dinner", "diet": "vegetarian", "calories": 520, "protein": 20, "carbs": 65, "fat": 20, "ingredients": ["paneer","tomato","cream","rice","spices"],"image_url":"https://www.bitesofberi.com/wp-content/uploads/2020/10/paneer-tikka-masala-1.jpg"},
{"name": "Grilled Fish with Sweet Potato", "meal_type": "Dinner", "diet": "non-vegetarian", "calories": 510, "protein": 36, "carbs": 45, "fat": 18, "ingredients": ["fish","sweet potato","olive oil","lemon"],"image_url":"https://img.taste.com.au/yWpI_V2_/taste/2017/01/crumbed-fish-with-sweet-potato-chips_1980x1320-119628-1.jpg"},
{"name": "Tofu & Veggie Curry", "meal_type": "Dinner", "diet": "vegetarian", "calories": 460, "protein": 18, "carbs": 60, "fat": 15, "ingredients": ["tofu","cauliflower","peas","coconut milk","spices"],"image_url":"https://assets.bonappetit.com/photos/5d4b5b39e9887a0008135935/1:1/w_2560%2Cc_limit/BA-0919-Tofu-Summer-Veggie-Curry.jpg"},
{"name": "Chicken Fajitas", "meal_type": "Dinner", "diet": "non-vegetarian", "calories": 550, "protein": 40, "carbs": 50, "fat": 18, "ingredients": ["chicken","bell pepper","onion","tortilla"],"image_url":"https://easyweeknightrecipes.com/wp-content/uploads/2021/07/grilled-chicken-fajitas-6.jpg"},
{"name": "Vegetable Lasagna", "meal_type": "Dinner", "diet": "vegetarian", "calories": 500, "protein": 22, "carbs": 60, "fat": 18, "ingredients": ["pasta","cheese","spinach","tomato","zucchini"],"image_url":"https://cdn.loveandlemons.com/wp-content/uploads/2023/12/vegetarian-lasagna-scaled.jpg"},
{"name": "Turkey Meatballs with Zoodles", "meal_type": "Dinner", "diet": "non-vegetarian", "calories": 530, "protein": 38, "carbs": 35, "fat": 20, "ingredients": ["turkey","zucchini","tomato sauce","spices"],"image_url":"https://www.eatwell101.com/wp-content/uploads/2018/04/turkey-meatballs-recipe.jpg"},
{"name": "Chickpea & Spinach Stew", "meal_type": "Dinner", "diet": "vegetarian", "calories": 470, "protein": 18, "carbs": 60, "fat": 14, "ingredients": ["chickpeas","spinach","tomato","onion","spices"],"image_url":"https://www.eatingwell.com/thmb/PqRN1f14fA3zdvpFMGi7I19FCPU=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/hearty-chickpea-spinach-stew-270568-1x1-b27d319be4504a39ba4d4184d1a3b2cb.jpg"},
{"name": "Beef Stir Fry with Broccoli", "meal_type": "Dinner", "diet": "non-vegetarian", "calories": 560, "protein": 42, "carbs": 40, "fat": 20, "ingredients": ["beef","broccoli","soy sauce","garlic"],"image_url":"https://natashaskitchen.com/wp-content/uploads/2019/08/Beef-and-Broccoli-2.jpg"},
{"name": "Vegetable Korma with Rice", "meal_type": "Dinner", "diet": "vegetarian", "calories": 500, "protein": 18, "carbs": 70, "fat": 16, "ingredients": ["cauliflower","peas","carrot","cream","rice"],"image_url":"https://www.secondrecipe.com/wp-content/uploads/2022/02/vegetable-korma.jpg"},
{"name": "Garlic Butter Shrimp Pasta", "meal_type": "Dinner", "diet": "non-vegetarian", "calories": 580, "protein": 35, "carbs": 60, "fat": 22, "ingredients": ["shrimp","pasta","garlic","butter"],"image_url":"https://amyinthekitchen.com/wp-content/uploads/2022/05/Pasta-with-garlic-butter-shrimp-recipe.jpg"},
{"name": "Stuffed Zucchini Boats", "meal_type": "Dinner", "diet": "vegetarian", "calories": 470, "protein": 16, "carbs": 55, "fat": 14, "ingredients": ["zucchini","rice","tomato","cheese","spices"],"image_url":"https://www.spendwithpennies.com/wp-content/uploads/2024/05/1200-Stuffed-Zucchini-Boats-2-SpendWithPennies.jpg"},
{"name": "Grilled Lamb Chops with Veggies", "meal_type": "Dinner", "diet": "non-vegetarian", "calories": 600, "protein": 40, "carbs": 30, "fat": 25, "ingredients": ["lamb","zucchini","carrot","olive oil"],"image_url":"https://images.immediate.co.uk/production/volatile/sites/30/2020/08/recipe-image-legacy-id-984602_11-63dfe51.jpg"},
{"name": "Paneer Tikka with Quinoa", "meal_type": "Dinner", "diet": "vegetarian", "calories": 480, "protein": 22, "carbs": 50, "fat": 18, "ingredients": ["paneer","quinoa","bell pepper","spices"],"image_url":"https://mytastycurry.com/wp-content/uploads/2024/07/Quinoa-paneer-Salad.jpg"},
{"name": "Seared Tuna with Vegetables", "meal_type": "Dinner", "diet": "non-vegetarian", "calories": 520, "protein": 38, "carbs": 30, "fat": 20, "ingredients": ["tuna","broccoli","carrot","olive oil"],"image_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRo5S_LA5aI7tZWJOcHNr1EQbLs4g-25V3OKQ&s"},
{"name": "Cauliflower & Potato Curry", "meal_type": "Dinner", "diet": "vegetarian", "calories": 450, "protein": 14, "carbs": 65, "fat": 15, "ingredients": ["cauliflower","potato","tomato","spices"],"image_url":"https://www.teaforturmeric.com/wp-content/uploads/2018/04/Cauliflower-and-Potato-Curry-Aloo-Gobi-Recipe.jpg"},
{"name": "Chicken & Vegetable Stir Fry", "meal_type": "Dinner", "diet": "non-vegetarian", "calories": 550, "protein": 42, "carbs": 45, "fat": 18, "ingredients": ["chicken","broccoli","carrot","soy sauce"],"image_url":"https://bellyfull.net/wp-content/uploads/2021/02/Chicken-and-Vegetable-Stir-Fry-blog.jpg"},
{"name": "Spinach & Lentil Dal", "meal_type": "Dinner", "diet": "vegetarian", "calories": 470, "protein": 18, "carbs": 60, "fat": 12, "ingredients": ["lentils","spinach","onion","tomato","spices"],"image_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRjBBMgljLLGm-POE6VAibOuLwVExRFODw6gA&s"},
{"name": "Grilled Prawns with Rice", "meal_type": "Dinner", "diet": "non-vegetarian", "calories": 510, "protein": 36, "carbs": 40, "fat": 16, "ingredients": ["prawns","rice","lemon","olive oil"],"image_url":"https://www.lecremedelacrumb.com/wp-content/uploads/2019/05/one-pan-spanish-shrimp-rice-1-500x500.jpg"},
{"name": "Stuffed Cabbage Rolls", "meal_type": "Dinner", "diet": "vegetarian", "calories": 460, "protein": 16, "carbs": 60, "fat": 14, "ingredients": ["cabbage","rice","lentils","tomato"],"image_url":"https://www.allrecipes.com/thmb/XfBt4brgnhTZkigUEca6RU5uS94=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/26661-Stuffed-Cabbage-Rolls-ddmfs-4x3-62d721db9b4445ceb9273ceb18cd3bed.jpg"},
{"name": "Beef & Vegetable Stew", "meal_type": "Dinner", "diet": "non-vegetarian", "calories": 580, "protein": 40, "carbs": 45, "fat": 20, "ingredients": ["beef","carrot","potato","celery","spices"],"image_url":"https://twokooksinthekitchen.com/wp-content/uploads/2022/03/IMG_0309.jpg"},
{"name": "Tofu & Spinach Stir Fry", "meal_type": "Dinner", "diet": "vegetarian", "calories": 480, "protein": 20, "carbs": 55, "fat": 15, "ingredients": ["tofu","spinach","carrot","soy sauce"],"image_url":"https://pestoandpotatoes.com/wp-content/uploads/2024/09/TofuSpinachStirFry.jpg"},
{"name": "Roast Chicken with Veggies", "meal_type": "Dinner", "diet": "non-vegetarian", "calories": 600, "protein": 40, "carbs": 35, "fat": 22, "ingredients": ["chicken","carrot","zucchini","olive oil"],"image_url":"https://www.jocooks.com/wp-content/uploads/2020/03/roasted-chicken-and-vegetables-1-9.jpg"},
{"name": "Vegetable Shepherd's Pie", "meal_type": "Dinner", "diet": "vegetarian", "calories": 500, "protein": 18, "carbs": 65, "fat": 18, "ingredients": ["potato","carrot","peas","cheese","cream"],"image_url":"https://themindfulhapa.com/wp-content/uploads/2020/11/vegetarian-shepherds-pies-4.jpg"},
{"name": "Salmon Teriyaki with Veggies", "meal_type": "Dinner", "diet": "non-vegetarian", "calories": 520, "protein": 38, "carbs": 40, "fat": 20, "ingredients": ["salmon","broccoli","carrot","teriyaki sauce"],"image_url":"https://www.skinnytaste.com/wp-content/uploads/2016/12/Sheet-Pan-Teriyaki-Salmon-1-6.jpg"},

# ---------- SNACKS ----------
{"name": "Protein Smoothie", "meal_type": "Snack", "diet": "vegetarian", "calories": 250, "protein": 10, "carbs": 35, "fat": 8, "ingredients": ["banana","milk","almonds","peanut butter"],"image_url":"https://ichef.bbci.co.uk/food/ic/food_16x9_1600/recipes/protein_shake_21728_16x9.jpg"},
{"name": "Boiled Eggs & Apple", "meal_type": "Snack", "diet": "non-vegetarian", "calories": 200, "protein": 14, "carbs": 18, "fat": 9, "ingredients": ["eggs","apple"],"image_url":"https://i.pinimg.com/736x/ec/40/18/ec40183707ecb4919e218175da8e1c31.jpg"},
{"name": "Greek Yogurt with Honey", "meal_type": "Snack", "diet": "vegetarian", "calories": 180, "protein": 10, "carbs": 20, "fat": 6, "ingredients": ["greek yogurt","honey","walnuts"],"image_url":"https://assets.wholefoodsmarket.com/recipes/923/2048/1536/923-4.jpg"},
{"name": "Chana Chaat", "meal_type": "Snack", "diet": "vegetarian", "calories": 220, "protein": 12, "carbs": 30, "fat": 6, "ingredients": ["chickpeas","onion","tomato","lemon","spices"],"image_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTgz9OGr5RmgctI7I1qSMyJS5CSHuIeuh_UoQ&s"},
{"name": "Mixed Nuts", "meal_type": "Snack", "diet": "vegetarian", "calories": 300, "protein": 8, "carbs": 12, "fat": 26, "ingredients": ["almonds","cashews","walnuts"],"image_url":"https://m.media-amazon.com/images/I/51fJzWgwcSL._UF1000,1000_QL80_.jpg"},
{"name": "Fruit Salad", "meal_type": "Snack", "diet": "vegetarian", "calories": 150, "protein": 2, "carbs": 35, "fat": 1, "ingredients": ["apple","banana","orange","grapes"],"image_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRRYC1iWHEsd2CZ1G_xYDlXQWScN66TIWWeLg&s"},
{"name": "Carrot Sticks with Hummus", "meal_type": "Snack", "diet": "vegetarian", "calories": 180, "protein": 5, "carbs": 20, "fat": 9, "ingredients": ["carrot","hummus"],"image_url":"https://www.healthylittlefoodies.com/wp-content/uploads/2017/01/carrot-hummus-500x375.gif"},
{"name": "Cottage Cheese Cubes", "meal_type": "Snack", "diet": "vegetarian", "calories": 160, "protein": 14, "carbs": 6, "fat": 8, "ingredients": ["cottage cheese"],"image_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTp2_909jN5-JaJcUz2ne9MorkPtbuJaE-k8w&s"},
{"name": "Peanut Butter Toast", "meal_type": "Snack", "diet": "vegetarian", "calories": 220, "protein": 8, "carbs": 28, "fat": 10, "ingredients": ["bread","peanut butter"],"image_url":"https://40aprons.com/wp-content/uploads/2014/03/peanut-butter-banana-toast-1-1.jpg"},
{"name": "Energy Bars", "meal_type": "Snack", "diet": "vegetarian", "calories": 250, "protein": 9, "carbs": 35, "fat": 10, "ingredients": ["oats","honey","nuts","raisins"],"image_url":"https://www.wearesovegan.com/wp-content/uploads/2020/11/veganhomemadeenergybarst.jpg"},
{"name": "Boiled Chickpeas", "meal_type": "Snack", "diet": "vegetarian", "calories": 200, "protein": 12, "carbs": 30, "fat": 5, "ingredients": ["chickpeas","salt","spices"],"image_url":"https://www.vegrecipesofindia.com/wp-content/uploads/2022/07/chickpea-salad.jpg"},
{"name": "Apple with Peanut Butter", "meal_type": "Snack", "diet": "vegetarian", "calories": 180, "protein": 5, "carbs": 25, "fat": 8, "ingredients": ["apple","peanut butter"],"image_url":"https://www.valyastasteofhome.com/wp-content/uploads/2016/03/Easy-Apple-Snack-Recipe-Kids-Approved-Healthy-Snacks-4-500x375.jpg"},
{"name": "Trail Mix", "meal_type": "Snack", "diet": "vegetarian", "calories": 300, "protein": 8, "carbs": 30, "fat": 18, "ingredients": ["nuts","raisins","seeds"],"image_url":"https://www.eatingbirdfood.com/wp-content/uploads/2022/11/superfood-trail-mix-hero.jpg"},
{"name": "Vegetable Soup", "meal_type": "Snack", "diet": "vegetarian", "calories": 150, "protein": 5, "carbs": 20, "fat": 4, "ingredients": ["carrot","beans","peas","spices"],"image_url":"https://static01.nyt.com/images/2023/10/12/multimedia/LH-vegetable-soup-ckfp-copy/LH-vegetable-soup-ckfp-mediumSquareAt3X.jpg"},
{"name": "Cheese and Crackers", "meal_type": "Snack", "diet": "vegetarian", "calories": 200, "protein": 10, "carbs": 18, "fat": 10, "ingredients": ["cheese","crackers"],"image_url":"https://www.bklynlarder.com/cdn/shop/products/cheese-and-crackers-perfect-bite-gift-basket-755194_5000x5000.jpg?v=1695956285"},
{"name": "Roasted Almonds", "meal_type": "Snack", "diet": "vegetarian", "calories": 180, "protein": 6, "carbs": 6, "fat": 16, "ingredients": ["almonds"],"image_url":"https://www.allrecipes.com/thmb/ubezkKTj-UlQ1h_N8yIXPB6xiOI=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/229881-honey-roasted-almonds-DDMFS-beauty-4x3-BG-3074-d8368f28d9694d4d9ff565b280393a36.jpg"},
{"name": "Hard-Boiled Eggs", "meal_type": "Snack", "diet": "non-vegetarian", "calories": 150, "protein": 12, "carbs": 1, "fat": 10, "ingredients": ["eggs"],"image_url":"https://www.foodtasticmom.com/wp-content/uploads/2016/10/easyeggs-feature.jpg"},
{"name": "Banana with Almond Butter", "meal_type": "Snack", "diet": "vegetarian", "calories": 200, "protein": 5, "carbs": 27, "fat": 8, "ingredients": ["banana","almond butter"],"image_url":"https://thechiclife.com/wp-content/uploads/2018/07/BananaAlmondButterToast-0456.jpg"},
{"name": "Vegetable Spring Rolls", "meal_type": "Snack", "diet": "vegetarian", "calories": 220, "protein": 6, "carbs": 28, "fat": 10, "ingredients": ["cabbage","carrot","flour","spices"],"image_url":"https://d1mxd7n691o8sz.cloudfront.net/static/recipe/recipe/2023-12/Vegetable-Spring-Rolls-2-1-906001560ca545c8bc72baf473f230b4.jpg"},
{"name": "Edamame Beans", "meal_type": "Snack", "diet": "vegetarian", "calories": 180, "protein": 14, "carbs": 15, "fat": 8, "ingredients": ["edamame","salt"],"image_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQGVeeIJmccb0X-tR2ZJIOh_ImV8G1mP6yBpw&s"},
{"name": "Protein Balls", "meal_type": "Snack", "diet": "vegetarian", "calories": 200, "protein": 8, "carbs": 22, "fat": 9, "ingredients": ["oats","dates","peanut butter","cocoa"],"image_url":"https://i2.wp.com/lifemadesimplebakes.com/wp-content/uploads/2021/02/oatmeal-proten-balls-square-1200-1.jpg"},
{"name": "Hummus with Pita Bread", "meal_type": "Snack", "diet": "vegetarian", "calories": 210, "protein": 7, "carbs": 25, "fat": 10, "ingredients": ["hummus","pita bread"],"image_url":"https://www.electroluxarabia.com/globalassets/elux-arabia/inspiration/recipe/hummus-with-pita-bread_x3rl.jpg"},
{"name": "Cucumber Slices with Yogurt Dip", "meal_type": "Snack", "diet": "vegetarian", "calories": 150, "protein": 6, "carbs": 10, "fat": 7, "ingredients": ["cucumber","yogurt","spices"],"image_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSLXWbEB398LY63kQ342BnX-r8taqLu-bv80A&s"},
{"name": "Avocado Toast", "meal_type": "Snack", "diet": "vegetarian", "calories": 220, "protein": 6, "carbs": 28, "fat": 12, "ingredients": ["bread","avocado"],"image_url":"https://www.spendwithpennies.com/wp-content/uploads/2022/09/Avocado-Toast-SpendWithPennies-1.jpg"},
{"name": "Rice Cakes with Peanut Butter", "meal_type": "Snack", "diet": "vegetarian", "calories": 180, "protein": 6, "carbs": 24, "fat": 8, "ingredients": ["rice cakes","peanut butter"],"image_url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSrOsw-FnnMEjPOaDHBlydzBZWInvB2cAj_9Q&s"},
{"name": "Pumpkin Seeds", "meal_type": "Snack", "diet": "vegetarian", "calories": 150, "protein": 7, "carbs": 5, "fat": 12, "ingredients": ["pumpkin seeds"],"image_url":"https://www.jessicagavin.com/wp-content/uploads/2017/10/roasted-pumpkin-seeds-savory-1200.jpg"},
{"name": "Roasted Chickpeas", "meal_type": "Snack", "diet": "vegetarian", "calories": 200, "protein": 12, "carbs": 28, "fat": 5, "ingredients": ["chickpeas","spices"],"image_url":"https://greatcurryrecipes.net/wp-content/uploads/2014/02/roastchickpeas6-735x980.jpg"},
{"name": "Sweet Potato Fries", "meal_type": "Snack", "diet": "vegetarian", "calories": 220, "protein": 4, "carbs": 35, "fat": 8, "ingredients": ["sweet potato","olive oil","salt"],"image_url":"https://cdn.loveandlemons.com/wp-content/uploads/2024/01/sweet-potato-fries.jpg"},
{"name": "Yogurt Parfait", "meal_type": "Snack", "diet": "vegetarian", "calories": 180, "protein": 8, "carbs": 20, "fat": 5, "ingredients": ["yogurt","granola","berries"],"image_url":"https://spicecravings.com/wp-content/uploads/2023/09/Greek-Yogurt-Parfait-Featured.jpg"},
{"name": "Almond Butter Celery Sticks", "meal_type": "Snack", "diet": "vegetarian", "calories": 150, "protein": 5, "carbs": 8, "fat": 12, "ingredients": ["celery","almond butter"],"image_url":"https://www.midwestliving.com/thmb/TyK2qsg0t5v8hfnZnokfQ3TpZ-8=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/102907755_asian-ants-on-a-log-44565c9df1d846c0ba500b8a267213b6.jpg"}


]
# Load or create user data file
def load_user_data():
    try:
        with open("user_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_user_data(data):
    with open("user_data.json", "w") as file:
        json.dump(data, file, indent=4)
def filter_meals(meal_list, user_data):
    diet = user_data.get("diet")
    goal = user_data.get("goal")
    include = user_data.get("include_ingredients", [])
    exclude = user_data.get("exclude_ingredients", [])

    filtered = []

    for meal in meal_list:
        # Filter by diet
        if diet and meal["diet"] != diet:
            continue

        # Filter by goal
        if goal == "weight_loss" and meal["calories"] > 500:
            continue
        elif goal == "muscle_gain" and meal["protein"] < 20:
            continue
        elif goal == "keto" and meal["carbs"] > 20:
            continue

        # Include ingredients
        if include and not any(ing.lower() in meal["ingredients"] for ing in include):
            continue

        # Exclude ingredients
        if exclude and any(ing.lower() in meal["ingredients"] for ing in exclude):
            continue

        filtered.append(meal)

    return filtered

@app.route("/", methods=["GET", "POST"])
def home():
    user_data = {}
    recommended_meals = []

    if request.method == "POST":
        # Get user input
        diet = request.form.get("diet")
        allergies = request.form.get("allergies", "").split(",")
        calories = request.form.get("calories", "")
        meal_type = request.form.get("meal_type")

        # Convert calories safely
        try:
            calories = int(calories)
        except:
            calories = 0

        # Save user input
        user_data = {
            "diet": diet,
            "allergies": [a.strip().lower() for a in allergies if a.strip()],
            "calories": calories,
            "meal_type": meal_type,
        }

        # Save to JSON
        with open("user_data.json", "w") as f:
            json.dump(user_data, f, indent=4)

        # Apply filters
        for meal in meals:
            print("\nChecking meal:", meal["name"])
            match = True

            # Diet filter
            if user_data["diet"] and meal["diet"] != user_data["diet"]:
                print("❌ Excluded by diet")
                match = False

            # Meal type filter
            if user_data["meal_type"] and meal["meal_type"].lower() != user_data["meal_type"].lower():
                print("❌ Excluded by meal type")
                match = False

            # Allergy filter
            if user_data["allergies"]:
                if any(ingredient.lower() in user_data["allergies"] for ingredient in meal["ingredients"]):
                    print("❌ Excluded by allergy match")
                    match = False

            # Calories filter (±100 kcal tolerance)
            if user_data["calories"] and not (meal["calories"] <= user_data["calories"] + 100):
                print("❌ Excluded by calories")
                match = False

            if match:
                recommended_meals.append(meal)
                print("✅ Added:", meal["name"])

        # If nothing matches, suggest closest meals
        if not recommended_meals and user_data.get("calories", 0) > 0:
            recommended_meals = sorted(meals, key=lambda m: abs(m["calories"] - user_data["calories"]))[:2]
            print("⚠️ No exact match found. Showing closest meals.")

        # Debug prints
        print("\n=== User Preferences ===")
        print(user_data)
        print("=== Final Recommended Meals ===")
        print(recommended_meals)

    return render_template(
        "dashboard.html",
        recommended_meals=recommended_meals,
        meals=meals,
        user_data=user_data
    )




if __name__ == "__main__":
    app.run(debug=True)
