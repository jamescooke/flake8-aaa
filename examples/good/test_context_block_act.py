from project.auth import user_perms_changed

from .helpers import catch_signal


def test(api_client, url):
    data = {
        'user_id': 0,
        'project_permission': 'admin',
    }

    with catch_signal(user_perms_changed) as callback:
        result = api_client.put(url, data=data)

    assert result.status_code == 400
    assert callback.call_count == 0
