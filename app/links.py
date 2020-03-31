from event_calendar.model.link import Link
import app.handlers as handlers

search = handlers.search_for(Link)
get    = handlers.get_for(Link)
post   = handlers.post_for(Link)
update = handlers.update_for(Link)
delete = handlers.delete_for(Link)
