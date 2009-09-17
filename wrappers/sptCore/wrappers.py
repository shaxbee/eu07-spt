import os
from pyplusplus import messages
from pyplusplus.module_builder import call_policies

classes = ['Path', 'RailTracking', 'Track']

def wrap(mb):
    opaque = {
        'Path': ['reverse'],
        'RailTracking': ['getPath'],
        'Track': ['getPath', 'getDefaultPath']
    }

    mb.class_('Path').include();
    mb.class_('RailTracking').include();
    mb.class_('Track').include();

    for className, methods in opaque.items():
        cls = mb.class_(className);
        for functionName in methods:
            cls.member_function(functionName).call_policies = call_policies.return_value_policy(call_policies.reference_existing_object);

    #Creating code creator. After this step you should not modify/customize declarations.
    mb.build_code_creator( module_name='sptCore' )

