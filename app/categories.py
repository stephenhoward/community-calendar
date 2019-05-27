from flask import Blueprint
from event_calendar.model.category import Category
import app.handlers as handlers

categories = Blueprint('categories',__name__)

search = handlers.search_for(Category)
get    = handlers.get_for(Category)
post   = handlers.post_for(Category)
update = handlers.update_for(Category)
delete = handlers.delete_for(Category)
