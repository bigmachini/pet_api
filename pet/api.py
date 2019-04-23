from flask.views import MethodView
from flask import jsonify, request, abort
from app.decorators import app_required


class PetAPI(MethodView):
    decorators = [app_required]

    pets = [{"id": 1, "name": u"Mac", "links": [{"rel": "self", "href": "/pets/1"}]},
            {"id": 2, "name": u"Leo", "links": [
                {"rel": "self", "href": "/pets/2"}]},
            {"id": 3, "name": u"Brownie", "links": [{"rel": "self", "href": "/pets/3"}]}]

    def get(self, pet_id):
        if pet_id:
            response = {"pets": self.pets[pet_id-1]}
        else:
            response = {"pets": self.pets}
        return jsonify(response), 200

    def post(self):
        if not request.json or not 'name' in request.json:
            abort(400)

        pet_id = len(self.pets) + 1
        pet = {
            'id': pet_id,
            'name': request.json['name'],
            'links': [{"rel": "self", "href": "/pets/{}".format(pet_id)}]
        }

        self.pets.append(pet)
        return jsonify({'pet': pet}), 201

    def put(self, pet_id):
        if not request.json or not 'name' in request.json:
            abort(400)

        pet = self.pets[pet_id - 1]
        pet['name'] = request.json['name']
        return jsonify({'pet': pet}), 200

    def delete(self, pet_id):
        print('pet_id: {}'.format(pet_id))
        if len(self.pets) > 0:
            del self.pets[pet_id - 1]
            return jsonify({}), 204
        else:
            print(self.pets)
            abort(400)
