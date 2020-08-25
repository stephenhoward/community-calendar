from event_calendar.model.link import Link
import app.handlers as handlers
from app.guards import guard_content

search = guard_content( Link, method = handlers.search )
get    = guard_content( Link, method = handlers.get    )
post   = guard_content( Link, method = handlers.post   )
update = guard_content( Link, method = handlers.update )
delete = guard_content( Link, method = handlers.delete )
