import pytest
from tcrypt.tcrypt import TCrypt


def test_tcrypt_without_option(capsys):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        TCrypt()
    out, err = capsys.readouterr()
    assert 'usage: tcrypt [-h] [--version]' in out
    assert 'error: one of the arguments' in err
    assert 'is required' in err
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2

def test_tcrypt_with_non_existent_param(capsys, monkeypatch):
    monkeypatch.setattr('sys.argv', ['pytest', '-test'])
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        TCrypt()
    out, err = capsys.readouterr()
    assert 'usage: tcrypt [-h] [--version]' in out
    assert 'error: one of the arguments' in err
    assert 'is required' in err
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2

def test_tcrypt_help(capsys, monkeypatch):
    monkeypatch.setattr('sys.argv', ['pytest', '-h'])
    try:
        TCrypt()
    except SystemExit:
        pass
    out, err = capsys.readouterr()
    assert err == ''
    assert 'Interface for handling truecrypt files.' in out
    assert '-h, --help' in out
    assert '--version' in out
    assert '-i <dir>, --init <dir>' in out
    assert '-s, --stop' in out
    assert '-l, --list' in out
    assert '-m <file>, --mount <file>' in out
    assert '-d, --dismount' in out
    assert 'Proctect your data! :-)' in out

def test_tcrypt_version(capsys, monkeypatch):
    monkeypatch.setattr('sys.argv', ['pytest', '--version'])
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        TCrypt()
    out, err = capsys.readouterr()
    assert err == ''
    assert 'TCrypt version:' in out
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0

def test_tcrypt_init(capsys, monkeypatch):
    monkeypatch.setattr('sys.argv', ['pytest', '-i', 'dir'])
    TCrypt()
    out, err = capsys.readouterr()
    assert out == '' and err == ''

def test_tcrypt_init_without_param(capsys, monkeypatch):
    monkeypatch.setattr('sys.argv', ['pytest', '-i'])
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        TCrypt()
    out, err = capsys.readouterr()
    assert 'usage: tcrypt [-h] [--version]' in out
    assert 'argument -i/--init: expected one argument' in err
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2

def test_tcrypt_stop(capsys, monkeypatch):
    monkeypatch.setattr('sys.argv', ['pytest', '-s'])
    TCrypt()
    out, err = capsys.readouterr()
    assert out == '' and err == ''

def test_tcrypt_stop_with_param(capsys, monkeypatch):
    monkeypatch.setattr('sys.argv', ['pytest', '-s', 'file'])
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        TCrypt()
    out, err = capsys.readouterr()
    assert 'usage: tcrypt [-h] [--version]' in out
    assert 'unrecognized arguments' in err
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2

def test_tcrypt_list(capsys, monkeypatch):
    monkeypatch.setattr('sys.argv', ['pytest', '-l'])
    TCrypt()
    out, err = capsys.readouterr()
    assert out == '' and err == ''

def test_tcrypt_list_with_param(capsys, monkeypatch):
    monkeypatch.setattr('sys.argv', ['pytest', '-l', 'file'])
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        TCrypt()
    out, err = capsys.readouterr()
    assert 'usage: tcrypt [-h] [--version]' in out
    assert 'unrecognized arguments' in err
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2

def test_tcrypt_mount(capsys, monkeypatch):
    monkeypatch.setattr('sys.argv', ['pytest', '-m', 'file'])
    TCrypt()
    out, err = capsys.readouterr()
    assert out == '' and err == ''

def test_tcrypt_mount_without_param(capsys, monkeypatch):
    monkeypatch.setattr('sys.argv', ['pytest', '-m'])
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        TCrypt()
    out, err = capsys.readouterr()
    assert 'usage: tcrypt [-h] [--version]' in out
    assert 'argument -m/--mount: expected one argument' in err
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2

def test_tcrypt_dismount(capsys, monkeypatch):
    monkeypatch.setattr('sys.argv', ['pytest', '-d'])
    TCrypt()
    out, err = capsys.readouterr()
    assert out == '' and err == ''

def test_tcrypt_dismount_with_param(capsys, monkeypatch):
    monkeypatch.setattr('sys.argv', ['pytest', '-d', 'file'])
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        TCrypt()
    out, err = capsys.readouterr()
    assert 'usage: tcrypt [-h] [--version]' in out
    assert 'unrecognized arguments' in err
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2

def test_tcrypt_error(capsys, monkeypatch):
    monkeypatch.setattr('sys.argv', ['pytest', '-d'])
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        tcript = TCrypt()
        tcript.error('not found error')
    out, err = capsys.readouterr()
    assert 'usage: tcrypt [-h] [--version]' in out
    assert 'not found' in err
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2
