from event_calendar.model.series import Series
from event_calendar.model.image import Image
import app.handlers as handlers

search = handlers.search_for(Series)
get    = handlers.get_for(Series)
post   = handlers.post_for(Series)
update = handlers.update_for(Series)
delete = handlers.delete_for(Series)

post_image = handlers.upload_file_for(Image)
get_image  = handlers.serve_file_for(Image)