from event_calendar.model.org import Org
import app.handlers as handlers

search = handlers.search_for(Org)
get    = handlers.get_for(Org)
post   = handlers.post_for(Org)
update = handlers.update_for(Org)
delete = handlers.delete_for(Org)
