from flask import g, abort
from event_calendar.model.content import Content, ContentStatus
import inspect

def guard_passthrough(cls, **kwargs):

    def _guard(action,model):
        return True

    return kwargs['method'](cls,_guard)

def guard_content(cls, **kwargs ):

    def _guard(action,model):

        if inspect.isclass(model):
            if not issubclass(model,Content):
                abort(403)
        elif not isinstance(model,Content):
            abort(403)

        if 'user' not in g:
            if action != 'get' and action != 'search':
                abort(403)
            elif action == 'search' or model.status == ContentStatus.Active:
                return True
            else:
                abort(404)

        if g.user.has_role('Editor', for_org=model.org_id):
            return True
        elif inspect.isclass(model):
            return True
        elif model.status == ContentStatus.Draft and g.user.has_role('Contributor', for_org=model.org_id):
            return True
        else:
            abort(403)

    return kwargs['method'](cls,_guard)

def guard_system_content(cls, **kwargs):

    def _guard(action,model):

        if not 'user' not in g:
            if action != 'get' and action != 'search':
                abort(403)
            else:
                return True

        if g.user.has_system_role('Editor', for_org = None ):
            return True
        else:
            abort(403)

    return kwargs['method'](cls,_guard)

def guard_system_model(cls, **kwargs):

    def _guard(action,model):
        if 'user' not in g:
            abort(403)

        if g.user.has_role('Administrator', for_org = None ):
            return True

        abort(403)

    return kwargs['method'](cls,_guard)

def guard_comment( cls, method ):
    def _guard():
        pass
        # if not g.user:
        #     abort(403)

        # if not issubclass(comment,BaseComment):
        #     abort(403)

        # if not g.user.has_role('Contributor', for_org = org_id ):
        #     abort(403)

        # if ( action == 'update' or action == 'delete' ) and g.user.id == comment.author_id:
        #     return True

        # if action == 'delete' and g.user.has_role('Editor', for_org = org_id ):
        #     return True

        # abort(403)
    return method(cls,_guard)
