from event_calendar.model.series import Series
import app.handlers as handlers
from app.guards import guard_content

search = guard_content( Series, method = handlers.search )
get    = guard_content( Series, method = handlers.get    )
post   = guard_content( Series, method = handlers.post   )
update = guard_content( Series, method = handlers.update )
delete = guard_content( Series, method = handlers.delete )
