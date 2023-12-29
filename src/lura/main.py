from plug.qt import AppPlug

class Lura(AppPlug):
    pass

def run():

    app=Lura()
    app.activate()
    app.run()
