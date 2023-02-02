import subprocess


class Truecrypt:
    def __init__(self, name='tcrypt') -> None:
        self.container = None
        self.status = False
        self.error = None
        self.__initialize(name)

    def __str__(self) -> str:
        if self.container:
            return f'Truecrypt: {self.status}\n'\
                f'Container: \n'\
                f'\tId: {list(self.container.values())[0]}\n'\
                f'\tImage: {list(self.container.values())[1]}\n'\
                f'\tCommand: {list(self.container.values())[2]}\n'\
                f'\tCreated: {list(self.container.values())[3]}\n'\
                f'\tStatus: {list(self.container.values())[4]}\n'\
                f'\tPorts: {list(self.container.values())[5]}\n'\
                f'\tName: {list(self.container.values())[6]}\n'
        return f'Truecrypt: {self.status}'

    def start(self) -> bool:
        pass

    def stop(self) -> bool:
        pass
    def mount(self) -> bool:
        pass
    def dismount(self) -> bool:
        pass
    def list(self) -> bool:
        pass

    def __initialize(self, name) -> None:
        output = self.__check_docker(name)
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

    def __check_docker(self, name) -> None:
        output, error = self.__exec_command(
            f'docker container ls | grep {name}'
        )
        if 'command not found' in error:
            self.error = 'you need to install docker'
        elif not output and not error:
            self.error = 'truecrypt container not found'
        elif 'permission denied' in error.lower():
            self.error = 'user have no permission to connect to the docker'
        else:
            output = output.split('\n', maxsplit=1)[0].split('  ')
            return [field for field in output if field.strip() != '']
        return None

    def __container_parser(self, data) -> dict:
        if len(data) == 6:
            return {
                'id': data[0],
                'image': data[1].strip().split(':')[0],
                'command': data[2].strip().strip('"'),
                'created': data[3],
                'status': data[4],
                'ports': '',
                'name': data[5].strip()
            }
        elif len(data) == 7:
            return {
                'id': data[0],
                'image': data[1].strip().split(':')[0],
                'command': data[2].strip().strip('"'),
                'created': data[3],
                'status': data[4],
                'ports': data[5],
                'name': data[6].stip()
            }
        else:
            return False

    def __get_container_info(self, data) -> None:
        if data:
            container = self.__container_parser(data)
            if container:
                self.status = True
                self.container = container
            else:
                self.error = 'container truecrypt is not working'
