from refer_bot.handlers import admin, start, user

# in this file import all the sub-modules that contain the handlers
# the modules here will be visible to getmembers() of this handlers package
# all handlers in the exposed modules will be added to the client
# in other words "export" the modules that contain the handlers here
