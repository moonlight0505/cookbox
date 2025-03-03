from flask import Flask, request, redirect, url_for # type: ignore

app = Flask(__name__)

user_data = {}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST": 
        user_data["name"] = request.form.get("name", "Guest")
        return redirect(url_for("preferences"))

    return f"""
    <html>
    <head>
        <title>CookBox</title>
        <style>
            body {{
                text-align: center;
                margin-top: 10%;
                font-family: Arial, sans-serif;
            }}
            h1 {{ color: royalblue; }}
            h2 {{ color: cornflowerblue; }}
            input, button {{
                padding: 10px;
                font-size: 16px;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <h1>Welcome to Cookbox!</h1>
        <h2>Your ultimate destination for delicious recipes.</h2>

        <form method="POST"> 
            <label for="name">Enter your name:</label>
            <input type="text" id="name" name="name" required>
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    """

@app.route("/Preferences", methods=["GET", "POST"])
def preferences():
    name = user_data.get("name", "Guest") 
    
    if request.method == "POST":
        user_data["dietary"] = request.form.get("dietary", "None")
        user_data["cuisine"] = request.form.get("cuisine", "None")
        user_data["meals_per_week"] = request.form.get("meals", "0")
        
        return redirect(url_for("recipe_input"))

    return f"""
    <html>
    <head>
        <title>Preferences</title>
        <style>
            body {{
                text-align: center;
                margin-top: 10%;
                font-family: Arial, sans-serif;
            }}
            h1 {{ color: royalblue; }}
            h2 {{ color: cornflowerblue; }}
            imput, button {{
                padding: 10px;
                font-size: 14px;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <h1>Hello, {name}!</h1>
        <h2>Tell us more about your food preferences:</h2>

        <form method="POST">
            <label for="dietary">Dietary Restrictions:</label>
            <input type="text" id="dietary" name="dietary" placeholder="e.g., Vegetarian, Gluten-Free" required><br><br>

            <label for="cuisine">Favorite Cuisine:</label>
            <input type="text" id="cuisine" name="cuisine" placeholder="e.g., Italian, Mexican" required><br><br>

            <label for="meals">Number of Meals per Week:</label>
            <input type="number" id="meals" name="meals" min="1" required><br><br>

            <button type="submit">Submit Preferences</button>
        </form>
    </body>
    </html>
    """

@app.route("/recipe_input", methods=["GET", "POST"])
def recipe_input():
    if request.method == "POST":
        recipe_name = request.form.get("recipe_name", "No Recipe Name")
        ingredients = request.form.get("ingredients", "No Ingredients")
        
        if "recipes" not in user_data:
            user_data["recipes"] = []

        user_data["recipes"].append({
            "recipe_name": recipe_name,
            "ingredients": ingredients
        })
        
        return redirect(url_for("recipe_plan"))
        
    name = user_data.get("name", "Guest")
    return f"""
    <html>
    <head>
        <title>Recipe Input</title>
        <style>
            body {{
                text-align: center;
                margin-top: 10%;
                font-family: Arial, sans-serif;
            }}
            h1 {{ color: royalblue; }}
            input, textarea, button {{
                padding: 10px;
                font-size: 16px;
                margin-top: 10px;
            }}
        </style>
    </head>
    <body>
        <h1>Recipe Input for {name}</h1>
        <form method="POST">
            <label for="recipe_name">Recipe Name:</label>
            <input type="text" id="recipe_name" name="recipe_name" required><br><br>
            <label for="ingredients">Ingredients:</label><br>
            <textarea id="ingredients" name="ingredients" rows="5" cols="30" required></textarea><br><br>
            <button type="submit">Submit Recipe</button>
        </form>
    </body>
    </html>
    """   

@app.route("/recipe_plan")
def recipe_plan():
    name = user_data.get("name", "Guest")
    dietary = user_data.get("dietary", "None")
    cuisine = user_data.get("cuisine", "None")
    meals = user_data.get("meals_per_week", "0")
    recipes = user_data.get("recipes", [])

    filtered_recipes = recipes
    if recipes:
        if dietary != "None":
            filtered_recipes = [r for r in filtered_recipes
                                if dietary.lower() in r["ingredients"].lower() or dietary.lower() in r["recipe_name"].lower()]
        if cuisine != "NOne":
            filtered_recipes = [r for r in filtered_recipes
                                if cuisine.lower() in r["ingredients"].lower() or cuisine.lower() in r["recipe_name"].lower()]
    
    if not recipes:
        recipes_list = "<p>You have not entered any recipes yet. Please enter a recipe.</p>"
    elif not filtered_recipes:
        recipes_list = "<p>No recipes match your dietary restrictions and cuisine preferences. Please enter more recipes.</p>"
    else:
        recipes_list = "<ul>"
        for recipe in recipes:
            recipes_list += f"<li><b>{recipe['recipe_name']}</b>: {recipe['ingredients']}</li>"
        recipes_list += "</ul>"
    
    return f"""
    <html>
    <head>
        <title>Recipe Plan</title>
        <style>
            body {{
                text-align: center;
                margin-top: 10%;
                font-family: Arial, sans-serif;
            }}
            h1 {{
                color: royalblue;
            }}
            h2 {{
                color: cornflowerblue;
            }}
            ul {{
                list-style-type: none;
                padding: 0;
            }}
            li {{
                margin: 10px 0;
            }}
            button {{
                padding: 10px;
                font-size: 16px;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>{name}'s Recipe Plan</h1>
        <h2>Your Preferences</h2>
        <p><b>Dietary Restrictions:</b> {dietary}</p>
        <p><b>Favorite Cuisine:</b> {cuisine}</p>
        <p><b>Meals per Week:</b> {meals}</p>
        {recipes_list}
        <form action="/Preferences" method="GET">
            <button type="submit">Back to Preferences</button>
        </form>
    </body>
    </html>
    """
