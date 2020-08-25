from event_calendar.model.location import Location
import app.handlers as handlers
from app.guards import guard_content

search = guard_content( Location, method = handlers.search )
get    = guard_content( Location, method = handlers.get    )
post   = guard_content( Location, method = handlers.post   )
update = guard_content( Location, method = handlers.update )
delete = guard_content( Location, method = handlers.delete )
