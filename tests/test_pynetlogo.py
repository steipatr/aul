import pyNetLogo

netlogo = pyNetLogo.NetLogoLink(gui=True)

netlogo.load_model('Fire.nlogo')

netlogo.kill_workspace()