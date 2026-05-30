import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=False)
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL environment variable is not set")

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    ingredients = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=False) 
with app.app_context():
    db.create_all()
@app.route("/recipes", methods=["POST"])
def add_recipe():
    data = request.get_json(force=True)

    name = (data.get("name") or "").strip()
    category = (data.get("category") or "").strip()
    ingredients = (data.get("ingredients") or "").strip()
    description = (data.get("description") or "").strip()

    if not name or not description:
        return jsonify({"error": "name and description are required"}), 400

    recipe = Recipe(
        name=name,
        category=category or None,
        ingredients=ingredients or None,
        description=description
    )
    db.session.add(recipe)
    db.session.commit()

    return jsonify({"status": "ok", "id": recipe.id}), 201

@app.route("/recipes", methods=["GET", "OPTIONS"])
def get_recipes():
    recipes = Recipe.query.order_by(Recipe.id.desc()).all()
    return jsonify([
        {
            "id": r.id,
            "name": r.name,
            "category": r.category,
            "ingredients": r.ingredients,
            "description": r.description
        } for r in recipes
    ])

@app.route("/recipes/<int:recipe_id>", methods=["DELETE"])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"status": "deleted"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(host="0.0.0.0", port=5000, debug=True)