from truecrypt import Truecrypt
from tcrypt import TCrypt


if __name__ == '__main__':
    tcrypt = TCrypt()
    true = Truecrypt()

    if tcrypt.args.init:
        print('Initializing truecrypt container...')
        if not true.start(tcrypt.args.init):
            tcrypt.error(true.error)
    elif tcrypt.args.stop:
        print('Stopping truecrypt container...')
        if not true.stop():
            tcrypt.error(true.error)
