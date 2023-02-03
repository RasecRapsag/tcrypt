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
def test_truecrypt_docker_container_not_working(mock_subprocess):
    output = b'6a1caa751e0e   rrapsag/truecrypt'\
             b'  2 minutes ago  Up 2 minutes  tcrypt\n'
    mock_subprocess.return_value = process_mock(output, b'')
    true = Truecrypt()
    assert not true.status
    assert 'container truecrypt is not working' in true.error

@patch('subprocess.Popen')
def test_truecrypt_docker_container_name_already_in_use(mock_subprocess):
    output = b'6a1caa751e0e   rrapsag/truecrypt  "/entrypoint.sh"'\
             b'  21 minutes ago  Exited (137) 21 minutes  tcrypt\n'
    mock_subprocess.return_value = process_mock(output, b'')
    true = Truecrypt()
    assert not true.status
    assert 'container name "tcrypt" is already in use' in true.error

@patch('subprocess.Popen')
def test_truecrypt_docker_container_wrong_image(mock_subprocess):
    output = b'6a1caa751e0e   nginx  "/entrypoint.sh"'\
             b'  54 minutes ago  Up 54 minutes  tcrypt\n'
    mock_subprocess.return_value = process_mock(output, b'')
    true = Truecrypt()
    assert not true.status
    assert 'container truecrypt is not running from valid image' in true.error

@patch('subprocess.Popen')
def test_truecrypt_docker_container_status_ok(mock_subprocess):
    output = b'6a1caa751e0e   rrapsag/truecrypt  "/entrypoint.sh"'\
             b'  54 minutes ago  Up 54 minutes  tcrypt\n'
    mock_subprocess.return_value = process_mock(output, b'')
    true = Truecrypt()
    assert true.status and true.error is None

@patch('subprocess.Popen')
def test_truecrypt_class_print_str_invalid_image(mock_subprocess):
    output = b'6a1caa751e0e   nginx  "/entrypoint.sh"'\
             b'  54 minutes ago  Up 54 minutes  tcrypt\n'
    mock_subprocess.return_value = process_mock(output, b'')
    true = Truecrypt()
    assert not true.status
    assert 'Truecrypt: False' in str(true)
    assert 'Error: container truecrypt is not running from valid image' in str(true)

@patch('subprocess.Popen')
def test_truecrypt_class_print_str_already_in_use(mock_subprocess):
    output = b'6a1caa751e0e   rrapsag/truecrypt  "/entrypoint.sh"'\
             b'  54 minutes ago  Exited (137) 54 minutes  tcrypt\n'
    mock_subprocess.return_value = process_mock(output, b'')
    true = Truecrypt()
    assert not true.status
    assert 'Truecrypt: False' in str(true)
    assert 'Error: container name "tcrypt" is already in use' in str(true)

@patch('subprocess.Popen')
def test_truecrypt_class_print_str_ok(mock_subprocess):
    output = b'6a1caa751e0e   rrapsag/truecrypt  "/entrypoint.sh"'\
             b'  54 minutes ago  Up 54 minutes  tcrypt\n'
    mock_subprocess.return_value = process_mock(output, b'')
    true = Truecrypt()
    assert true.status and true.error is None
    assert 'Truecrypt: True' in str(true)
    assert 'Id: 6a1caa751e0e' in str(true)
    assert 'Image: rrapsag/truecrypt' in str(true)
    assert 'Name: tcrypt' in str(true)

@patch('subprocess.Popen')
def test_truecrypt_container_start_unable_find_image(mock_subprocess):
    error = b"Unable to find image 'rrapsag/truecrypt1:latest' locally"\
            b"docker: Error response from daemon: manifest for "\
            b"rrapsag/truecrypt1:latest not found: manifest unknown: "\
            b"manifest unknown.\nSee 'docker run --help'."
    mock_subprocess.return_value = process_mock(b'', error)
    true = Truecrypt()
    true.start('/mnt')
    assert not true.status
    assert 'unable to find image' in true.error

@patch('subprocess.Popen')
def test_truecrypt_container_start_ok(mock_subprocess):
    output = b'6a1caa751e0e   rrapsag/truecrypt  "/entrypoint.sh"'\
             b'  54 minutes ago  Up 54 minutes  tcrypt\n'
    mock_subprocess.return_value = process_mock(output, b'')
    true = Truecrypt()
    true.start('/mnt')
    assert true.status and true.error is None
    assert 'rrapsag/truecrypt' in true.container['image']
    assert 'tcrypt' in true.container['name']
    assert 'up' in true.container['status'].lower()
