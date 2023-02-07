import subprocess
import getpass


class Truecrypt:
    def __init__(self, name='tcrypt') -> None:
        self.container = None
        self.status = False
        self.error = None
        self.__initialize(name)

    def start(self, volume) -> bool:
        if not self.status:
            cmd = f"docker run -d --privileged --rm --name {self.container['name']} "\
                  f'-v {volume}:/crypt rrapsag/truecrypt'
            output, error = self.__exec_command(cmd)
            if error:
                self.status = False
                self.container = output
                if 'not found' in self.__extract_error(error):
                    self.error = 'unable to find image truecrypt'
                else:
                    self.error = self.__extract_error(error)
            else:
                self.status = True
                self.error = None
                return True
        else:
            self.status = False
            self.error = 'truecrypt container has already been started'
        return False

    def stop(self) -> bool:
        if self.status and self.container:
            cmd = f"docker stop {self.container['id']}"
            output, error = self.__exec_command(cmd)
            if not error and output.strip() == self.container['id']:
                return True
        return False

    def mount(self, file) -> bool:
        if self.status and self.container:
            passwd = self.__check_password()
            if passwd:
                cmd = f"truecrypt --mount --non-interactive "\
                      f"--fs-options='uid=1000,gid=984,umask=000' "\
                      f"-p {passwd} /crypt/{file} /mnt/truecrypt"
                output, error = self.__docker_exec(cmd)
                print(f'OUTPUT: {output}')
                print(f'ERROR: {error}')
                if error:
                    self.status = False
                    self.error = self.__extract_error(error)
                else:
                    return True
        return False

    def dismount(self) -> bool:
        pass
    def list(self) -> bool:
        pass

    def __initialize(self, name) -> None:
        self.container = {'name': name}
        output = self.__check_docker()
        self.__get_container_info(output)

    def __exec_command(self, cmd) -> str:
        execute = subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, error = execute.communicate()
        return output.decode('utf-8'), error.decode('utf-8')

    def __check_docker(self) -> None:
        output, error = self.__exec_command(
            f"docker container ls -a | grep {self.container['name']}"
        )
        if 'command not found' in error:
            self.error = 'you need to install docker'
        elif 'permission denied' in error.lower():
            self.error = 'user have no permission to connect to the docker'
        elif 'Exited (' in output:
            self.container = None
            self.error = 'container name "tcrypt" is already in use'
        elif not output and not error:
            self.error = 'truecrypt container not found'
        else:
            output = output.split('\n', maxsplit=1)[0].split('  ')
            return [field for field in output if field.strip() != '']
        return None

    def __container_parser(self, data) -> dict:
        container = {
            'id': data[0],
            'image': data[1].strip().split(':')[0],
            'command': data[2].strip().strip('"'),
            'created': data[3].strip(),
            'status': data[4].strip()
        }
        if container['image'] != 'rrapsag/truecrypt':
            self.error = 'container truecrypt is not running from valid image'
        elif len(data) > 5:
            if len(data) == 6:
                container.update({'ports': '', 'name': data[5].strip()})
            elif len(data) == 7:
                container.update({'ports': data[5].strip(), 'name': data[6].strip()})
            return container
        return {}

    def __get_container_info(self, data) -> None:
        if data:
            container = self.__container_parser(data)
            if container:
                self.status = True
                self.container = container
            elif self.error is not None:
                self.container = None
            else:
                self.container = None
                self.error = 'container truecrypt is not working'

    def __extract_error(self, error) -> str:
        error = error.split(':')
        words = ('not found', 'incorrect', 'no such', 'failed to', 'already mounted')
        for err in error:
            for word in words:
                if word in err.lower():
                    return err.strip().lower().split('\n')[0].replace('.', '').replace('\'', '')

    def __check_password(self) -> str:
        passwd = getpass.getpass().strip()
        if not passwd:
            self.status = False
            self.error = 'blank password is not allowed'
            return False
        return passwd

    def __docker_exec(self, cmd):
        cmd = f"docker exec {self.container['id']} {cmd}"
        return self.__exec_command(cmd)

    def __str__(self) -> str:
        if self.container and len(self.container) > 1:
            return f'Truecrypt: {self.status}\n'\
                f'Container: \n'\
                f'\tId: {list(self.container.values())[0]}\n'\
                f'\tImage: {list(self.container.values())[1]}\n'\
                f'\tCommand: {list(self.container.values())[2]}\n'\
                f'\tCreated: {list(self.container.values())[3]}\n'\
                f'\tStatus: {list(self.container.values())[4]}\n'\
                f'\tPorts: {list(self.container.values())[5]}\n'\
                f'\tName: {list(self.container.values())[6]}\n'
        return f'Truecrypt: {self.status}\nError: {self.error}'
