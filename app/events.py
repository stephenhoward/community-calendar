from event_calendar.model.event import Event
from event_calendar.model.image import EventImage
import app.handlers as handlers

search = handlers.search_for(Event)
get    = handlers.get_for(Event)
post   = handlers.post_for(Event)
update = handlers.update_for(Event)
delete = handlers.delete_for(Event)

post_image = handlers.upload_file_for(EventImage)
get_image  = handlers.serve_file_for(EventImage)