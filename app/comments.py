from event_calendar.model.comment import Comment,Reply
import app.handlers as handlers

add_comment    = handlers.post_comment_for(Comment)
get_comments   = handlers.get_comments_for(Comment)
update_comment = handlers.update_comment_for(Comment)
update_reply   = handlers.update_comment_for(Reply)
add_reply      = handlers.post_comment_for(Reply)
get_replies    = handlers.get_comments_for(Comment)
