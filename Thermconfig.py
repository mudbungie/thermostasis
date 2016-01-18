from configobj import ConfigObj
import os.path

whereAmI = os.path.dirname(os.path.abspath(__file__)) + '/'
config = ConfigObj(whereAmI + 'thermostasis.conf')
