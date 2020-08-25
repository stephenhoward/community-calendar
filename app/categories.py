from event_calendar.model.category import Category
import app.handlers as handlers
from app.guards import guard_system_content

search = guard_system_content( Category, method = handlers.search )
get    = guard_system_content( Category, method = handlers.get    )
post   = guard_system_content( Category, method = handlers.post   )
update = guard_system_content( Category, method = handlers.update )
delete = guard_system_content( Category, method = handlers.delete )
