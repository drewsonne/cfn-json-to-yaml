from yaml.dumper import Dumper
from yaml.representer import SafeRepresenter

class CleanDumper(Dumper):
   pass

CleanDumper.add_representer(str,
       SafeRepresenter.represent_str)

CleanDumper.add_representer(unicode,
        SafeRepresenter.represent_unicode)
