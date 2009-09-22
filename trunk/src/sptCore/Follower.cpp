#include <sptCore/Follower.h>

#include <assert.h>

#include <sptCore/Math.h>
#include <sptCore/Track.h>
#include <sptCore/Scenery.h>

using namespace sptCore;

Follower::Follower(Track& track, float distance):
    _track(&track), _distance(distance)
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

float segmentLength(Path::const_iterator& iter)
{
    return (*iter - *(iter - 1)).length();
};

std::pair<Path::const_iterator, float> Follower::findPosition() const
{

    Path::const_iterator iter = _path->begin() + 1;
    float distance = segmentLength(iter); 

    // find point location on path matching distance
    for(iter; distance < _distance && iter != _path->end(); iter++)
        distance += segmentLength(iter);

    // if we didn't found segment it means that _distance is wrong
    assert(iter != _path->end());

    // ratio = position in segment / segment length
    float ratio = (distance - _distance) / segmentLength(iter);

    return std::make_pair(iter, ratio);

}; // Follower::findPosition

osg::Vec3 Follower::getPosition() const
{

    Path::const_iterator iter;
    float ratio;

    boost::tie(iter, ratio) = findPosition();

    return (*(iter - 1) * ratio) + (*iter * (1 - ratio));

}; // Follower::getPosition

osg::Matrix Follower::getMatrix() const
{

    Path::const_iterator iter;
    float ratio;

    // find current segment and position in it expressed in (0, 1) range
    boost::tie(iter, ratio) = findPosition();

    osg::Vec3 begin(*(iter-1));
    osg::Vec3 end(*iter);

    // for first segment direction is equal to begin control vector
    osg::Vec3 dirBegin = (iter == _path->begin() + 1 ? _path->frontDir() : (end - begin));

    // for last segment direction is equal to end control vector
    osg::Vec3 dirEnd = (iter == _path->end() - 1 ? _path->backDir() : (*(iter + 1) - end));

    // create rotation matrix for given direction vector
    osg::Matrix transform(rotationMatrix(mix(dirBegin, dirEnd, ratio)));
    transform.makeTranslate(mix(begin, end, ratio));

    return transform;

}; // Follower::getMatrix

void Follower::changeTrack(osg::Vec3 position)
{

    Sector* sector = &(_track->getSector());
    osg::Vec3 offset(floor(position.x() / Sector::SIZE), floor(position.y() / Sector::SIZE), 0);

    // if position is outside current sector
    if(offset != osg::Vec3())
    {

        offset *= Sector::SIZE;
        sector = &(getScenery().getSector(sector->getPosition() + offset));
        position -= offset;

    };

    // register leaving previous track
    _track->leave(*this, position);

    try
    {
        _track = &(sector->getNextTrack(position, _track));
    }
    catch(Sector::UnknownConnectionException exc)
    {
        throw NullTrackException();
    };

    // if connection contained null track then sector is corrupt
    assert(_track != NULL);

    // update path
    _path = &(_track->getPath(position));

    // register entering track
    _track->enter(*this, _path->front());

}; // Follower::moveToNextTrack
