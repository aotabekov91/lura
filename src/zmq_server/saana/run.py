from .oliver import Oliver 

from tendo import singleton

def run():
    try:

        me=singleton.SingleInstance()

        app=Oliver()
        app.run()

    except singleton.SingleInstanceException:

        print('An instance of Oliver is already running!')
