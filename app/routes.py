from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.crystal import Crystal

#responsible for validating and returning crystal instance
def validate_crystal(crystal_id):
    try:
        crystal_id = int(crystal_id)
    except:
        abort(make_response({"message":f"crystal {crystal_id} is invalid type ({type(crystal_id)})"}, 400))
        
    crystal = Crystal.query.get(crystal_id)
    
    if not crystal:
        abort(make_response({"message": f"crystal {crystal_id} not found"}, 404))
    
    return crystal

crystal_bp = Blueprint("crystals", __name__, url_prefix="/crystals")

@crystal_bp.route('', methods=["POST"])
def handle_crystals():
    request_body = request.get_json()
    new_crystal = Crystal(
        name = request_body["name"],
        color = request_body["color"],
        powers = request_body["powers"]
    )
    
    db.session.add(new_crystal)
    db.session.commit()
    
    return make_response(f'Crystal {new_crystal.name} successfully created', 201)

@crystal_bp.route("", methods=["GET"])
def read_all_crystals():
    #filter the crystal query results
    #to those whose color match the query param
    color_query = request.args.get("color")
    powers_query = request.args.get("powers")
    
    if color_query:
        crystals = Crystal.query.filter_by(color=color_query)
    elif powers_query:
        crystals = Crystal.query.filter_by(powers=powers_query)
    else:
        crystals = Crystal.query.all()
    
    crystals_response = []
    for crystal in crystals:
        crystals_response.append(crystal.to_dict())
    return jsonify(crystals_response)

@crystal_bp.route("/<crystal_id>", methods=["GET"])
def read_one_crystal(crystal_id):
    crystal = validate_crystal(crystal_id)
    return crystal.to_dict(), 200
    
@crystal_bp.route('/<crystal_id>', methods=["PUT"])
def edit_crystal(crystal_id):
    crystal = validate_crystal(crystal_id)
    
    request_body = request.get_json()
    
    crystal.name = request_body['title']
    crystal.color = request_body['color']
    crystal.powers = request_body['powers']
    
    db.session.commit()
    
    return crystal.to_dict(), 200
    
@crystal_bp.route('/<crystal_id>', methods=["DELETE"])
def delete_crystal(crystal_id):
    crystal = validate_crystal(crystal_id)
    
    db.session.delete(crystal)
    db.session.commit()
    
    return make_response(f"Crystal #{crystal.id} deleted successfully", 200)