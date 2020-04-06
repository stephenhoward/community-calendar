from event_calendar.model.series import Series
import app.handlers as handlers

search = handlers.search_for(Series)
get    = handlers.get_for(Series)
post   = handlers.post_for(Series)
update = handlers.update_for(Series)
delete = handlers.delete_for(Series)
