import getpass
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
    error = b"Unable to find image 'rrapsag/truecrypt1:latest' locally\n"\
            b"docker: Error response from daemon: manifest for "\
            b"rrapsag/truecrypt1:latest not found: manifest unknown: "\
            b"manifest unknown.\nSee 'docker run --help'."
    mock_subprocess.return_value = process_mock(b'', error)
    true = Truecrypt()
    true.start('/mnt')
    assert not true.status
    assert 'unable to find image' in true.error

@patch('subprocess.Popen')
def test_truecrypt_container_has_already_been_started(mock_subprocess):
    output = b'6a1caa751e0e   rrapsag/truecrypt  "/entrypoint.sh"'\
             b'  54 minutes ago  Up 54 minutes  tcrypt\n'
    mock_subprocess.return_value = process_mock(output, b'')
    true = Truecrypt()
    true.start('/mnt')
    assert not true.status
    assert 'truecrypt container has already been started' in true.error

class FakeTruecrypt:

    @patch('subprocess.Popen')
    def return_truecrypt_not_started(self, mock_subprocess):
        mock_subprocess.return_value = process_mock(b'', b'')
        return Truecrypt()

    @patch('subprocess.Popen')
    def return_truecrypt_started(self, mock_subprocess):
        output = b'6a1caa751e0e   rrapsag/truecrypt  "/entrypoint.sh"'\
                 b'  54 minutes ago  Up 54 minutes  tcrypt\n'
        mock_subprocess.return_value = process_mock(output, b'')
        return Truecrypt()

@patch('subprocess.Popen')
def test_truecrypt_container_start_ok(mock_subprocess):
    true = FakeTruecrypt().return_truecrypt_not_started()
    output = b'5fcd75525da5\n'
    mock_subprocess.return_value = process_mock(output, b'')
    ret = true.start('/mnt')
    assert ret and true.status and true.error is None

@patch('subprocess.Popen')
def test_truecrypt_container_not_started_stop(mock_subprocess):
    true = FakeTruecrypt().return_truecrypt_not_started()
    output = b'6a1caa751e0e\n'
    mock_subprocess.return_value = process_mock(output, b'')
    ret = true.stop()
    assert ret is False
    assert true.status is not None

@patch('subprocess.Popen')
def test_truecrypt_container_stop_ok(mock_subprocess):
    true = FakeTruecrypt().return_truecrypt_started()
    output = b'6a1caa751e0e\n'
    mock_subprocess.return_value = process_mock(output, b'')
    ret = true.stop()
    assert ret and true.status

def test_truecrypt_mount_password_empty(monkeypatch):
    monkeypatch.setattr(getpass, 'getpass', lambda: '')
    true = FakeTruecrypt().return_truecrypt_started()
    ret = true.mount('filecrypt')
    assert ret is False and true.status is False
    assert 'blank password is not allowed' in true.error

@patch('subprocess.Popen')
def test_truecrypt_mount_password_wrong(mock_subprocess, monkeypatch):
    monkeypatch.setattr(getpass, 'getpass', lambda: 'wrongpassword')
    error = b'Error: Incorrect password or not a TrueCrypt volume.'
    mock_subprocess.return_value = process_mock(b'', error)
    true = FakeTruecrypt().return_truecrypt_started()
    ret = true.mount('filecrypt')
    assert ret is False and true.status is False
    assert 'incorrect password' in true.error

@patch('subprocess.Popen')
def test_truecrypt_mount_file_not_found(mock_subprocess, monkeypatch):
    monkeypatch.setattr(getpass, 'getpass', lambda: 'password')
    error = b'Error: No such file or directory:\n/crypt/filecrypt1'
    mock_subprocess.return_value = process_mock(b'', error)
    true = FakeTruecrypt().return_truecrypt_started()
    ret = true.mount('filecrypt1')
    assert ret is False and true.status is False
    assert 'no such file or directory' in true.error

@patch('subprocess.Popen')
def test_truecrypt_mount_point_not_found(mock_subprocess, monkeypatch):
    monkeypatch.setattr(getpass, 'getpass', lambda: 'password')
    error = b'Error: mount: mounting /dev/mapper/truecrypt1 '\
            b'on /mnt/truecrypt1 failed: No such file or directory'
    mock_subprocess.return_value = process_mock(b'', error)
    true = FakeTruecrypt().return_truecrypt_started()
    ret = true.mount('filecrypt')
    assert ret is False and true.status is False
    assert 'no such file or directory' in true.error

@patch('subprocess.Popen')
def test_truecrypt_mount_fail_to_setup_loop_device(mock_subprocess, monkeypatch):
    monkeypatch.setattr(getpass, 'getpass', lambda: 'password')
    error = b'Error: Failed to set up a loop device:\n/crypt/filecrypt'
    mock_subprocess.return_value = process_mock(b'', error)
    true = FakeTruecrypt().return_truecrypt_started()
    ret = true.mount('filecrypt')
    assert ret is False and true.status is False
    assert 'failed to set up a loop device' in true.error

@patch('subprocess.Popen')
def test_truecrypt_mount_volume_success(mock_subprocess, monkeypatch):
    monkeypatch.setattr(getpass, 'getpass', lambda: 'password')
    mock_subprocess.return_value = process_mock(b'', b'')
    true = FakeTruecrypt().return_truecrypt_started()
    ret = true.mount('filecrypt')
    assert ret and true.status and true.error is None

@patch('subprocess.Popen')
def test_truecrypt_dismount_resource_busy(mock_subprocess):
    error = b'Error: device-mapper: remove ioctl on '\
          b'truecrypt  failed: Resource busy\nCommand failed.'
    mock_subprocess.return_value = process_mock(b'', error)
    true = FakeTruecrypt().return_truecrypt_started()
    ret = true.dismount()
    assert ret is False and true.status is False
    assert 'resource busy' in true.error

@patch('subprocess.Popen')
def test_truecrypt_dismount_volume_success(mock_subprocess):
    mock_subprocess.return_value = process_mock(b'', b'')
    true = FakeTruecrypt().return_truecrypt_started()
    ret = true.dismount()
    assert ret and true.status and true.error is None
