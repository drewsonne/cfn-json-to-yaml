import json, sys, yaml

from cfnjsontoyaml.convertor import ConvertToMediary
from cfnjsontoyaml.yamlobject.unicode import CleanDumper


def print_to_string(document):
    return yaml.dump(
        document,
        Dumper=CleanDumper,
        encoding='utf-8',
        allow_unicode=True,
        explicit_start=True
    )


def convert(args=sys.argv[1:]):
    if args:
        with open(args[0]) as fp:
            json_document = fp.read()
    else:
        json_document = []
        for line in sys.stdin:
            json_document.append(line)

        json_document = "\n".join(json_document)

    document = json.loads(json_document)

    print print_to_string(ConvertToMediary(document).convert())


if __name__ == '__main__':
    convert()
