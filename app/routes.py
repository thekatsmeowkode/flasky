from flask import Blueprint, jsonify

class Crystal:
    def __init__(self, id, name, color, powers):
        self.id = id
        self.name = name
        self.color = color
        self.powers = powers

#create a list of crystals
crystals = [
    Crystal(1, "Amethyst", "Purple", "Infinite knowledge and wisdom"),
    Crystal(2, "Tiger's Eye", "Gold", "Confidence, Strength"),
    Crystal(3, "Rose Quartz", "Pink", "Love"),
    ]

crystal_bp = Blueprint("crystals", __name__, url_prefix="/crystals")