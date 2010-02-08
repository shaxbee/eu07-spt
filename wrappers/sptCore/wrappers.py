import os
from pyplusplus import messages
from pyplusplus.module_builder import call_policies

classes = ['Path', 'RailTracking', 'Track']

def wrap(mb):
    opaque = {
        'Path': ['reverse'],
        'RailTracking': ['getPath', 'getSector'] #,
#        'Track': ['getPath', 'getDefaultPath']
    }

    mb.class_('Path').include();

    RailTracking = mb.class_('RailTracking')
    RailTracking.include();
    RailTracking.include_files.extend(['sptCore/Sector.h', 'sptCore/Follower.h'])

    Track = mb.class_('Track')
    Track.include();
    Track.include_files.extend(['sptCore/Sector.h', 'sptCore/Follower.h'])

#    mb.class_('Path').member_function('reverse').call_policies = call_policies.return_value_policy(call_policies.reference_existing_object);

    for className, methods in opaque.items():
        cls = mb.class_(className);
        for functionName in methods:
            cls.member_function(functionName).call_policies = call_policies.return_value_policy(call_policies.reference_existing_object);

    #Creating code creator. After this step you should not modify/customize declarations.
    mb.build_code_creator( module_name='sptCore' )

