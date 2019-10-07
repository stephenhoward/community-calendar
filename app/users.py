from event_calendar.model.user import User
import app.handlers as handlers

search = handlers.search_for(User)
get    = handlers.get_for(User)
post   = handlers.post_for(User)
update = handlers.update_for(User)
delete = handlers.delete_for(User)
