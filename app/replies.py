from flask import g, abort
from event_calendar.model.comment import Comment,Reply
import app.handlers as handlers
from app.guards import guard_comment

search = guard_comment( Reply, handlers.search )
get    = guard_comment( Reply, handlers.get )
post   = guard_comment( Reply, handlers.post )
update = guard_comment( Reply, handlers.update )


def get_comments(cls):
    def get_comments(**kwargs):
        model = cls.get(kwargs['id'])
        return jsonify( model.comments )
    return get_comments


def post_comment_for(cls):
    def post(**kwargs):
        model   = cls.get(kwargs['id'])
        comment = model.add_comment(request.json)

        check_comment_authorized('create',comment,model.org_id)

        model.save()

        return jsonify( comment )
    return post

def update_comment_for(cls):
    def update(**kwargs):
        model = cls.get(kwargs['id'])

        if not model:
            abort(404)

        comment = model.get_comment(kwargs['comment_id'])

        if comment:
            check_comment_authorized('update',comment,model.org_id)
            comment.update( request.json ).save()
            return jsonify( comment )
        else:
            abort(404)
    return update

