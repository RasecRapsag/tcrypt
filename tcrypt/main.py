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
    elif tcrypt.args.mount:
        print('Mounting truecrypt volume...')
        if not true.mount(tcrypt.args.mount):
            tcrypt.error(true.error)
    elif tcrypt.args.dismount:
        print('Dismounting truecrypt volume...')
        if not true.dismount():
            tcrypt.error(true.error)
