from behave import *
from slackrest.command import Visibility, Method
import json


@given(u'a command with pattern \'{pattern}\'')
def step_impl(context, pattern):
    context.command_attributes['pattern'] = pattern


@given(u'URL format \'{url_format}\' with method {method}')
def step_impl(context, url_format, method):
    context.command_attributes['url_format'] = url_format
    context.command_attributes['method'] = Method.parse(method)


@given(u'URL format \'{url_format}\'')
def step_impl(context, url_format):
    context.command_attributes['url_format'] = url_format
    context.command_attributes['method'] = Method.GET


@given(u'for any visibility')
def step_impl(context):
    context.command_attributes['visibility'] = Visibility.Public


@given(u'with no request body')
def step_impl(context):
    context.command_attributes['body'] = None


@when(u'I send a message \'{msg}\'')
def step_impl(context, msg):
    command = type('ACommand', (object,), context.command_attributes)
    context.command_parser.add_command(command)

    channel_id = "C0123456"
    user_id = 'U012345'
    user_name = 'foo'
    context.request = context.command_parser.parse(msg, channel_id, user_id, user_name, context.self_name, Visibility.Public)


@when(u'a message \'{msg}\' is sent by user id \'{user_id}\'')
def step_impl(context, msg, user_id):
    command = type('ACommand', (object,), context.command_attributes)
    context.command_parser.add_command(command)
    channel_id = "C0123456"
    user_name = 'foo'
    context.request = context.command_parser.parse(msg, channel_id, user_id, user_name, context.self_name, Visibility.Public)


@when(u'a message \'{msg}\' is sent from channel \'{channel_id}\'')
def step_impl(context, msg, channel_id):
    command = type('ACommand', (object,), context.command_attributes)
    context.command_parser.add_command(command)
    user_id = 'U012345'
    user_name = 'foo'
    context.request = context.command_parser.parse(msg, channel_id, user_id, user_name, context.self_name, Visibility.Public)


@when(u'a message \'{msg}\' is sent by user name {user_name}')
def step_impl(context, msg, user_name):
    command = type('ACommand', (object,), context.command_attributes)
    context.command_parser.add_command(command)
    user_id = 'U012345'
    channel_id = 'C012345'
    context.request = context.command_parser.parse(msg, channel_id, user_id, user_name, context.self_name, Visibility.Public)


@when(u'I send a message \'{msg}\' in {visibility}')
def step_impl(context, msg, visibility):
    command = type('ACommand', (object,), context.command_attributes)
    context.command_parser.add_command(command)

    if visibility == 'public':
        channel_visibility = Visibility.Public
    elif visibility == 'private':
        channel_visibility = Visibility.Private
    else:
        raise ValueError('Unknown visibility "{}"'.format(visibility))

    channel_id = "C0123456"
    user_id = 'C012345'
    user_name = 'foo'
    context.request = context.command_parser.parse(msg, channel_id, user_id, user_name, context.self_name, channel_visibility)


@then(u'the request URL is \'{url}\'')
def step_impl(context, url):
    assert context.request.url == url


@then(u'the request body is empty')
def step_impl(context):
    assert context.request.body is None


@given(u'for private channels')
def step_impl(context):
    context.command_attributes['visibility'] = Visibility.Private


@then(u'the command is ignored')
def step_impl(context):
    assert context.request is None


def params_as_json(**kwargs):
    return json.dumps(kwargs)


@given(u'with a body that writes the param value as JSON')
def step_impl(context):
    context.command_attributes['body'] = params_as_json


@then(u'the request body contains \'{value}\'')
def step_impl(context, value):
    assert value in context.request.body


@then(u'the request method is {method}')
def step_impl(context, method):
    assert context.request.method == Method.parse(method)


def user_id_body(user_id, **kwargs):
    return json.dumps(user_id)


@given(u'with a body that contains the user id')
def step_impl(context):
    context.command_attributes['body'] = user_id_body


def channel_id_body(channel_id, **kwargs):
    return json.dumps(channel_id)


@given(u'with a body that contains the channel id')
def step_impl(context):
    context.command_attributes['body'] = channel_id_body


def user_name_body(user_name, **kwargs):
    return json.dumps(user_name)


@given(u'with a body that contains a user name')
def step_impl(context):
    context.command_attributes['body'] = user_name_body


@given(u'that the bot name is \'{botname}\'')
def step_impl(context, botname):
    context.self_name = botname


@given(u'there is a command which responds to anything')
def step_impl(context):
    context.command_attributes['pattern'] = '{anything}'
    context.command_attributes['url_format'] = '/'
    context.command_attributes['method'] = Method.GET
    context.command_attributes['visibility'] = Visibility.Any
    context.command_attributes['body'] = None
