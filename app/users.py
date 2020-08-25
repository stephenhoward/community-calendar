from event_calendar.model.user import User
import app.handlers as handlers
from app.guards import guard_system_model

search = guard_system_model( User, method = handlers.search )
get    = guard_system_model( User, method = handlers.get    )
post   = guard_system_model( User, method = handlers.post   )
update = guard_system_model( User, method = handlers.update )
delete = guard_system_model( User, method = handlers.delete )
