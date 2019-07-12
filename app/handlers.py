from flask import jsonify, request, abort

def search_for(cls):
    def search():
        q = cls.search(**request.args)
        return jsonify( q.all() )
    return search

def get_for(cls):
    def get(**kwargs):
        model = cls.get(kwargs['id'])

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