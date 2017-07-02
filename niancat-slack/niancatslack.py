from slackrest.app import SlackrestApp
from slackrest.command import Visibility, Method
import json


class GetPuzzle:
    pattern = '!nian'
    url_format = '/puzzle'
    visibility = Visibility.Any
    body = None
    method = Method.GET


class SetPuzzle:
    pattern = '!sättnian {nian}'
    url_format = '/puzzle'
    visibility = Visibility.Any
    method = Method.POST

    @classmethod
    def body(cls, nian, **kwargs):
        return json.dumps(nian)


class ListUnsolution:
    pattern = '!olösningar'
    url_format = '/unsolution/{user_id}'
    visibility = Visibility.Private
    method = Method.GET
    body = None


class AddUnsolution:
    pattern = '!olösning {unsolution}'
    url_format = '/unsolution/{user_id}'
    visibility = Visibility.Private
    method = Method.POST

    @classmethod
    def body(cls, unsolution, **kwargs):
        return json.dumps(unsolution)


class CheckSolution:
    pattern = '{solution}'
    url_format = '/solution'
    visibility = Visibility.Private
    method = Method.POST

    @classmethod
    def body(cls, solution, **kwargs):
        return json.dumps(solution)


class NiancatSlack(SlackrestApp):
    def __init__(self, base_url, notification_channel_id):
        commands = [GetPuzzle, SetPuzzle, ListUnsolution, AddUnsolution, CheckSolution]
        SlackrestApp.__init__(self, base_url, commands, notification_channel_id)


if __name__ == "__main__":
    app = NiancatSlack('http://niancat-chat', '#konsulatet')
    app.run_forever()