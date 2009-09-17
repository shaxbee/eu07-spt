#include <sptCore/Follower.h>

#include <sptCore/Track.h>
#include <sptCore/Scenery.h>

using namespace sptCore;

Follower::Follower(Track& track, float distance):
    _track(&track), _distance(distance), _sector(&track.getSector())
{
	
	_path = &track.getDefaultPath();

};

void Follower::move(float distance)
{
	
	_distance += distance;	

    while(_distance < 0)
    {
        
        changeTrack(_path->front());
        _distance += _path->length();

    };
	
	while(_distance > _path->length())
	{
	    
		_distance -= _path->length();
        changeTrack(_path->back());
				
	};
	
}; // Follower::move

void Follower::changeTrack(osg::Vec3 position)
{

        osg::Vec3 offset(floor(position.x() / Sector::SIZE), 0, floor(position.z() / Sector::SIZE));

        if(offset != osg::Vec3())
        {

            offset *= Sector::SIZE;
            _sector = &getScenery().getSector(getSector().getPosition() + offset);
            position -= offset;

        };

		_track->leave(*this, position);
		_track = &(_sector->getNextTrack(position, _track));
		
		if(_track == NULL)
			throw NullTrackException();

        if(_sector != &_track->getSector())
        {

            osg::Vec3 oldSector = _sector->getPosition();
            _sector = &_track->getSector();

    		_path = &_track->getPath(position + (oldSector - _sector->getPosition()));

        } 
        else 
        {

            _path = &_track->getPath(position);

        };

		_track->enter(*this, _path->front());

}; // Follower::moveToNextTrack
