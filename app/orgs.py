from event_calendar.model.org import Org
import app.handlers as handlers
from app.guards import guard_system_model

search = guard_system_model( Org, method = handlers.search )
get    = guard_system_model( Org, method = handlers.get    )
post   = guard_system_model( Org, method = handlers.post   )
update = guard_system_model( Org, method = handlers.update )
delete = guard_system_model( Org, method = handlers.delete )
