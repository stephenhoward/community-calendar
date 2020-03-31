from event_calendar.model.image import Image
import app.handlers as handlers

post_image = handlers.upload_file_for(Image)
get_image  = handlers.serve_file_for(Image)
