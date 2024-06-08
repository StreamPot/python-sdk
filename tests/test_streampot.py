import pytest
import requests_mock
from streampot import StreamPot, JobEntity, JobStatus


@pytest.fixture
def stream_pot():
    return StreamPot(secret='test_secret')


def test_initialization(stream_pot):
    assert stream_pot.secret == 'test_secret'
    assert stream_pot.base_url == 'https://api.streampot.io/v1'
    assert isinstance(stream_pot.actions, list)
    assert len(stream_pot.actions) == 0


def test_get_job(stream_pot):
    with requests_mock.Mocker() as m:
        job_id = 123
        mock_url = f"{stream_pot.base_url}/jobs/{job_id}"
        mock_response = {'id': 123, 'status': 'completed', 'created_at': '2020-01-01'}
        m.get(mock_url, json=mock_response)

        response = stream_pot.get_job(job_id)
        assert response.id == mock_response['id']
        assert response.status == JobStatus[mock_response['status'].upper()]
        assert response.created_at == mock_response['created_at']


def test_run(stream_pot):
    with requests_mock.Mocker() as m:
        mock_url = f"{stream_pot.base_url}/"
        mock_response = {'id': 124, 'status': 'pending', 'created_at': '2020-01-02'}
        m.post(mock_url, json=mock_response)

        response = stream_pot.run()
        assert isinstance(response, JobEntity)
        assert response.id == 124
        assert response.status == JobStatus.PENDING
        assert response.created_at == '2020-01-02'


def test_add_action(stream_pot):
    stream_pot.merge_add('source_video.mp4')
    assert len(stream_pot.actions) == 1
    assert stream_pot.actions[0]['name'] == 'mergeAdd'
    assert stream_pot.actions[0]['value'] == ['source_video.mp4']


@pytest.mark.parametrize("method, expected_action", [
    ("merge_add", 'mergeAdd'),
    ("add_input", 'addInput'),
    # add more methods and expected actions as necessary
])
def test_actions(stream_pot, method, expected_action):
    action_method = getattr(stream_pot, method)
    action_method('example_source')
    assert len(stream_pot.actions) == 1
    assert stream_pot.actions[0]['name'] == expected_action
    assert stream_pot.actions[0]['value'] == ['example_source']
