from flask import jsonify, request, abort

def search_for(cls):
    def search():
        return jsonify([
            {
                'id':   '12345',
                'info': [
                    {
                        'language': 'en',
                        'name': 'Test'
                    }
                ]
            }
        ])
    return search

def get_for(cls):
    def get(id):
        model = cls.get(id)

        if ( model ):
            return jsonify( model )
        else:
            abort(404)
    return get

def post_for(cls):
    def post():
        model = cls.create(request.json).save()

        return jsonify( model )
    return post

def update_for(cls):
    def update(id):
        model = cls.get(id)

        if ( model ):
            model.update( request.json ).save()
            return jsonify( model )
        else:
            abort(404)
    return update

def delete_for(cls):
    def delete(id):
        model = cls.get(id);

        if ( model ):
            model.delete()
            return jsonify( ok = 1 )
        else:
            abort(404)
    return delete