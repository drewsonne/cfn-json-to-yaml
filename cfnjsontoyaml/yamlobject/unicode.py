from yaml.dumper import Dumper
from yaml.representer import SafeRepresenter

class CleanDumper(Dumper):
   pass

if __name__ == 'cfnjsontoyaml.yamlobject.unicode':

    CleanDumper.add_representer(str,
           SafeRepresenter.represent_str)

    CleanDumper.add_representer(unicode,
            SafeRepresenter.represent_unicode)
