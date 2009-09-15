#include <sptCore/Follower.h>

#include <sptCore/Track.h>
#include <sptCore/Scenery.h>

using namespace sptCore;

Follower::Follower(Sector* sector, Track* track, float distance):
	_sector(sector), _track(track), _distance(distance)
{
	
	_path = track->getPath();

};

void Follower::move(float distance)
{
	
	_distance += distance;	
	
	while(_distance > _path->length())
	{
		
		_distance -= _path->length();
		
		osg::Vec3 next = _path->back();
		osg::Vec3 offset(floor(next.x() / Sector::SIZE), 0.0f, floor(next.z() / Sector::SIZE));
		
		if(offset != osg::Vec3())
		{
            osg::Vec3 sectorPosition = _sector->getPosition() +  offset * Sector::SIZE;
			setSector(&(_sector->getScenery().getSector(sectorPosition)));
			next -= offset * Sector::SIZE;
		};
				
		_track->leave(this, _path->back());
		_track = &(_sector->getNextTrack(next, _track));
		
		if(_track == NULL)
			throw NullTrackException();

		_path = _track->getPath(next);
		_track->enter(this, _path->front());
		
	};
	
}
