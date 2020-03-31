from event_calendar.model.location import Location
import app.handlers as handlers

search = handlers.search_for(Location)
get    = handlers.get_for(Location)
post   = handlers.post_for(Location)
update = handlers.update_for(Location)
delete = handlers.delete_for(Location)
