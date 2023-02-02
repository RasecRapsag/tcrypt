from unittest.mock import patch, Mock
from tcrypt.truecrypt import Truecrypt


def process_mock(output, error):
    mock = Mock()
    attrs = {'communicate.return_value': (output, error)}
    mock.configure_mock(**attrs)
    return mock

@patch('subprocess.Popen')
def test_truecrypt_docker_not_installed(mock_subprocess):
    mock_subprocess.return_value = process_mock(
        b'', b'command not found: docker'
    )
    true = Truecrypt()
    assert not true.status
    assert 'you need to install docker' in true.error

@patch('subprocess.Popen')
def test_truecrypt_docker_not_permission(mock_subprocess):
    mock_subprocess.return_value = process_mock(
        b'', b'Got permission denied while trying to connect'
    )
    true = Truecrypt()
    assert not true.status
    assert 'user have no permission to connect' in true.error

@patch('subprocess.Popen')
def test_truecrypt_docker_container_not_found(mock_subprocess):
    mock_subprocess.return_value = process_mock(b'', b'')
    true = Truecrypt()
    assert not true.status
    assert 'truecrypt container not found' in true.error

@patch('subprocess.Popen')
def test_truecrypt_docker_container_status_ok(mock_subprocess):
    output = b'6a1caa751e0e   rrapsag/truecrypt  "/entrypoint.sh"'\
             b'  54 minutes ago  Up 54 minutes  tcrypt\n'
    mock_subprocess.return_value = process_mock(output, b'')
    true = Truecrypt()
    assert true.status and true.error is None

@patch('subprocess.Popen')
def test_truecrypt_docker_container_not_working(mock_subprocess):
    output = b'6a1caa751e0e   rrapsag/truecrypt'\
             b'  2 minutes ago  Up 2 minutes  tcrypt\n'
    mock_subprocess.return_value = process_mock(output, b'')
    true = Truecrypt()
    assert not true.status
    assert 'container truecrypt is not working' in true.error

@patch('subprocess.Popen')
def test_truecrypt_class_print_str(mock_subprocess):
    output = b'6a1caa751e0e   rrapsag/truecrypt  "/entrypoint.sh"'\
             b'  54 minutes ago  Up 54 minutes  tcrypt\n'
    mock_subprocess.return_value = process_mock(output, b'')
    true = Truecrypt()
    assert true.status and true.error is None
    assert 'Truecrypt: True' in str(true)
    assert 'Id: 6a1caa751e0e' in str(true)
    assert 'Image: rrapsag/truecrypt' in str(true)
    assert 'Name: tcrypt' in str(true)
