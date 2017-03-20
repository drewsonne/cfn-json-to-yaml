from cfnjsontoyaml.yamlobject.base64 import Base64
from cfnjsontoyaml.yamlobject.equals import Equals
from cfnjsontoyaml.yamlobject.findinmap import FindInMap
from cfnjsontoyaml.yamlobject.fnand import And
from cfnjsontoyaml.yamlobject.fnif import If
from cfnjsontoyaml.yamlobject.fnnot import Not
from cfnjsontoyaml.yamlobject.fnor import Or
from cfnjsontoyaml.yamlobject.getatt import GetAtt
from cfnjsontoyaml.yamlobject.getazs import GetAZs
from cfnjsontoyaml.yamlobject.importvalue import ImportValue
from cfnjsontoyaml.yamlobject.join import Join
from cfnjsontoyaml.yamlobject.ref import Ref
from cfnjsontoyaml.yamlobject.select import Select
from cfnjsontoyaml.yamlobject.sub import Sub

FUNCTION_MAPPING = {
    'Ref': Ref,
    'Fn::Base64': Base64,
    'Fn::FindInMap': FindInMap,
    'Fn::GetAtt': GetAtt,
    'Fn::GetAZs':GetAZs,
    'Fn::ImportValue': ImportValue,
    'Fn::Join': Join,
    'Fn::Select': Select,
    'Fn::Sub': Sub,
    'Fn::And': And,
    'Fn::Equals': Equals,
    'Fn::If': If,
    'Fn::Not': Not,
    'Fn::Or': Or
}
