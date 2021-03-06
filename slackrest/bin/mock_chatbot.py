import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import json

test_event_handler = None
loop = tornado.ioloop.IOLoop.current()


class TestEventHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        global test_event_handler
        test_event_handler = self

    def on_message(self, message):
        pass

    def on_close(self):
        pass


def write_event(type, message=None):
    event = {'event': type}
    if message:
        event['message'] = message
    if test_event_handler:
        loop.add_callback(test_event_handler.write_message, event)


class ReplyHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps([{'response_type': 'reply', 'message': 'Some reply'}]))
        self.finish()
        write_event('reply')


class NotificationHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps([{'response_type': 'notification', 'message': 'Some notification'}]))
        self.finish()
        write_event('notification')


class MakeAPostHandler(tornado.web.RequestHandler):
    def post(self):
        self.write(json.dumps([{'response_type': 'reply', 'message': 'Make a post'}]))
        self.finish()
        write_event('reply')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/reply', ReplyHandler),
            (r'/notify', NotificationHandler),
            (r'/makeapost', MakeAPostHandler),
            (r'/test', TestEventHandler)
        ]

        settings = {
            'template_path': 'templates'
        }
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(80)
    tornado.ioloop.IOLoop.instance().start()