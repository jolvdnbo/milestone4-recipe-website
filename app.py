import os
from flask import Flask, render_template, redirect, url_for, Blueprint
from flask_pymongo import PyMongo, pymongo
from flask_paginate import Pagination

from bson.objectid import ObjectId
from classes import *

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'pat_doc_recipedb'
app.config["MONGO_URI"] = 'mongodb://admin:1Pfhr39Hdi4@ds119060.mlab.com:19060/pat_doc_recipedb'

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_recipes')
def get_recipes():
    page = get_page()
    _recipes=mongo.db.recipes.find().sort('upvotes', pymongo.DESCENDING)
    recipe_list = paginate_list(_recipes, page, 10)
    pagination = Pagination(page=page, total=_recipes.count(), record_name='recipes')
    return render_template("recipe.html", recipes=recipe_list, pagination=pagination)

@app.route('/search_recipes')
def search_recipes():
    
    _cuisines = mongo.db.cuisines.find().sort("cuisine_name")
    cuisine_list = [cuisine for cuisine in _cuisines]
    _allergens = mongo.db.allergens.find().sort("allergen_name")
    allergen_list = [allergen for allergen in _allergens]
    return render_template("searchrecipe.html", allergens = allergen_list, cuisines = cuisine_list)
    
@app.route('/find_recipe_by_name', methods=["POST"])
def find_recipe_by_name():
    page = get_page()
    search_term = {"recipe_name": {'$regex': request.form['recipe_name'], '$options': 'i'}}
    _recipes = mongo.db.recipes.find(search_term).sort('upvotes', pymongo.DESCENDING)
    matching_recipes = paginate_list(_recipes, page, 10)
    pagination = Pagination(page=page, total=_recipes.count(), record_name='recipes')
    return render_template("recipesfound.html", recipes=matching_recipes, pagination=pagination)
    
@app.route('/find_recipe_cuisine_name', methods=["POST"])
def find_recipe_cuisine_name():
    page = get_page()
    search_term = {"cuisine_name": request.form['cuisine_name']}
    _recipes = mongo.db.recipes.find(search_term).sort('upvotes', pymongo.DESCENDING)
    matching_recipes = paginate_list(_recipes, page, 10)
    pagination = Pagination(page=page, total=_recipes.count(), record_name='recipes')
    return render_template("recipesfound.html", recipes=matching_recipes, pagination=pagination)
    
@app.route('/find_recipe_allergen_name', methods=["POST"])
def find_recipe_allergen_name():
    page = get_page()
    search_term = {"allergens": request.form['allergens']}
    _recipes = mongo.db.recipes.find(search_term).sort('upvotes', pymongo.DESCENDING)
    matching_recipes = paginate_list(_recipes, page, 10)
    pagination = Pagination(page=page, total=_recipes.count(), record_name='recipes')
    return render_template("recipesfound.html", recipes=matching_recipes, pagination=pagination)

@app.route("/add_recipe")
def add_recipe():
    _recipes = mongo.db.recipes.find()
    recipe_list = [recipe for recipe in _recipes]
    _cuisines = mongo.db.cuisines.find()
    cuisine_list = [cuisine for cuisine in _cuisines]
    _allergens = mongo.db.allergens.find()
    allergen_list = [allergen for allergen in _allergens]
    return render_template("addrecipe.html", recipes = recipe_list, allergens = allergen_list, cuisines = cuisine_list)

@app.route('/insert_recipe', methods=["POST"])
def insert_recipe():
    recipes = mongo.db.recipes
    new_recipe = create_recipe()
    recipes.insert_one(new_recipe)
    return redirect(url_for('get_recipe'))    
    
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_recipes = mongo.db.recipes.find()
    cuisines = mongo.db.cuisines.find()
    allergens = mongo.db.allergens.find()
    return render_template("editrecipe.html", recipe=the_recipe, recipes=all_recipes, cuisines=cuisines, allergens=allergens)
    
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))

@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    updated_recipe = create_recipe()
    recipes.update({'_id': ObjectId(recipe_id)},{"$set": updated_recipe})
    return redirect(url_for('get_recipes'))
    
@app.route('/get_cuisines')
def get_cuisines():
    page = get_page()
    _cuisines = mongo.db.cuisines.find()
    cuisine_list = paginate_list(_cuisines, page, 10)
    pagination = Pagination(page=page, total=_cuisines.count(), record_name='cuisines')
    return render_template('cuisine.html', cuisines=cuisine_list, pagination=pagination)
    
@app.route("/add_cuisine")
def add_cuisine():
    _cuisines = mongo.db.cuisines.find()
    cuisine_list = [cuisine for cuisine in _cuisines]
    return render_template("addcuisine.html", cuisines = cuisine_list)    

@app.route('/insert_cuisine', methods=['POST'])
def insert_cuisine():
    cuisines = mongo.db.cuisines
    new_cuisine = create_cuisine()
    cuisines.insert_one(new_cuisine)
    return redirect(url_for('get_cuisines')) 
    
@app.route('/edit_cuisine/<cuisine_id>')
def edit_cuisine(cuisine_id):
    the_cuisine = mongo.db.cuisines.find_one({"_id": ObjectId(cuisine_id)})
    cuisines = mongo.db.cuisines.find()
    return render_template("editcuisine.html", cuisines=cuisines, cuisine=the_cuisine)
    
    
@app.route('/delete_cuisine/<cuisine_id>')
def delete_cuisine(cuisine_id):
    mongo.db.cuisines.remove({'_id': ObjectId(cuisine_id)})
    return redirect(url_for('get_cuisines'))
 
 
@app.route('/update_cuisine/<cuisine_id>', methods=['POST'])
def update_cuisine(cuisine_id):
    new_cuisine = create_cuisine()
    mongo.db.cuisines.update( {'_id': ObjectId(cuisine_id)},
       new_cuisine)
    return redirect(url_for('get_cuisines'))
    
@app.route('/get_allergens')
def get_allergens():
    page = get_page()
    _allergens = mongo.db.allergens.find()
    allergen_list = paginate_list(_allergens, page, 10)
    pagination = Pagination(page=page, total=_allergens.count(), record_name='allergens')
    return render_template('allergen.html', allergens=allergen_list, pagination=pagination)
    

@app.route("/add_allergen")
def add_allergen():
    _allergens = mongo.db.allergens.find()
    allergen_list = [allergen for allergen in _allergens]
    return render_template("addallergen.html", allergens = allergen_list)    

@app.route('/insert_allergen', methods=['POST'])
def insert_allergen():
    allergens = mongo.db.allergens
    new_allergen = create_allergen()
    allergens.insert_one(new_allergen)
    return redirect(url_for('get_allergens')) 
    
@app.route('/edit_allergen/<allergen_id>')
def edit_allergen(allergen_id):
    the_allergen = mongo.db.allergens.find_one({"_id": ObjectId(allergen_id)})
    allergens = mongo.db.allergens.find()
    return render_template("editallergen.html", allergens=allergens, allergen=the_allergen)
    
    
@app.route('/delete_allergen/<allergen_id>')
def delete_allergen(allergen_id):
    mongo.db.allergens.remove({'_id': ObjectId(allergen_id)})
    return redirect(url_for('get_allergens'))
 
 
@app.route('/update_allergen/<allergen_id>', methods=['POST'])
def update_allergen(allergen_id):
    new_allergen = create_allergen()
    mongo.db.allergens.update( {'_id': ObjectId(allergen_id)},
                             new_allergen)
    return redirect(url_for('get_allergens'))


@app.route('/upvote/<recipe_id>', methods=["POST"])
def upvote(recipe_id):
    mongo.db.recipes.update_one({"_id": ObjectId(recipe_id)}, { "$inc" :{'upvotes': 1}})
    return redirect(url_for('get_recipes'))



    
if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)