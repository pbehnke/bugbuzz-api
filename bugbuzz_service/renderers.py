from __future__ import unicode_literals

from pyramid.renderers import JSON
from pyramid.settings import asbool

from . import models


def session_adapter(session, request):
    settings = request.registry.settings
    return dict(
        id=session.guid,
        encrypted=session.encrypted,
        href='/sessions/{}'.format(session.guid),
        pubnub_subscribe_key=settings['pubnub.subscribe_key'],
        client_channel=session.client_channel_id,
        dashboard_channel=session.dashboard_channel_id,
        aes_iv=(
            session.aes_iv.encode('base64')
            if session.aes_iv is not None else None
        ),
        validation_code=session.validation_code,
        encrypted_code=(
            session.encrypted_code.encode('base64')
            if session.encrypted_code is not None else None
        ),
        created_at=session.created_at.isoformat(),
        updated_at=session.updated_at.isoformat(),
        files=[file.guid for file in session.files],
        breaks=[break_.guid for break_ in session.breaks],
    )


def event_adapter(event, request):
    return dict(
        id=event.guid,
        type=event.type,
        params=event.params,
        created_at=event.created_at.isoformat(),
        updated_at=event.updated_at.isoformat(),
    )


def break_adapter(break_, request):
    return dict(
        id=break_.guid,
        session=break_.session.guid,
        file=break_.file.guid,
        lineno=break_.lineno,
        local_vars=break_.local_vars.encode('base64'),
        aes_iv=(
            break_.aes_iv.encode('base64')
            if break_.aes_iv is not None else None
        ),
        created_at=break_.created_at.isoformat(),
        updated_at=break_.updated_at.isoformat(),
    )


def file_adapter(file_, request):
    return dict(
        id=file_.guid,
        session=file_.session.guid,
        filename=file_.filename,
        mime_type=file_.mime_type,
        content=file_.content.encode('base64'),
        aes_iv=(
            file_.aes_iv.encode('base64')
            if file_.aes_iv is not None else None
        ),
        created_at=file_.created_at.isoformat(),
        updated_at=file_.updated_at.isoformat(),
    )


def enum_symbol(enum_value):
    if enum_value is None:
        return enum_value
    return str(enum_value).lower()


def includeme(config):
    settings = config.registry.settings
    kwargs = {}
    cfg_key = 'api.json.pretty_print'
    pretty_print = asbool(settings.get(cfg_key, True))
    if pretty_print:
        kwargs = dict(sort_keys=True, indent=4, separators=(',', ': '))

    json_renderer = JSON(**kwargs)
    json_renderer.add_adapter(models.Session, session_adapter)
    json_renderer.add_adapter(models.Event, event_adapter)
    json_renderer.add_adapter(models.Break, break_adapter)
    json_renderer.add_adapter(models.File, file_adapter)
    config.add_renderer('json', json_renderer)
