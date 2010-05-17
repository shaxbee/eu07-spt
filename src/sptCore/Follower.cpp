#include <sptCore/Follower.h>

#include <assert.h>

#include <sptUtil/Math.h>

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

float segmentLength(osg::Vec3Array::const_iterator& iter)
{
    return (*iter - *(iter - 1)).length();
};

void Follower::findPosition(osg::ref_ptr<osg::Vec3Array> points, osg::Vec3Array::const_iterator& iter, float& ratio) const
{

    iter = points->begin() + 1;
    float distance = segmentLength(iter); 

    // find point location on path matching distance
    for(iter; distance < _distance && iter != points->end(); iter++)
        distance += segmentLength(iter);

    // if we didn't found segment it means that _distance is wrong
    assert(iter != points->end());

    // ratio = position in segment / segment length
    ratio = (distance - _distance) / segmentLength(iter);

}; // Follower::findPosition

osg::Vec3 Follower::getPosition() const
{

    osg::ref_ptr<osg::Vec3Array> points(_path->points());
    osg::Vec3Array::const_iterator iter;
    float ratio;

    findPosition(points, iter, ratio);

    return sptUtil::mix(*(iter - 1), *iter, ratio);

}; // Follower::getPosition

osg::Matrix Follower::getMatrix() const
{

    osg::ref_ptr<osg::Vec3Array> points(_path->points());
    osg::Vec3Array::const_iterator iter;
    float ratio;

    // find current segment and position in it expressed in (0, 1) range
    findPosition(points, iter, ratio);

    osg::Vec3 begin(*(iter-1));
    osg::Vec3 end(*iter);

    // for first segment direction is equal to begin control vector
    osg::Vec3 dirBegin = (iter == points->begin() + 1 ? _path->frontDir() : (end - begin));

    // for last segment direction is equal to end control vector
    osg::Vec3 dirEnd = (iter == points->end() - 1 ? _path->backDir() : (*(iter + 1) - end));

    // create rotation matrix for given direction vector
    osg::Matrix transform(sptUtil::rotationMatrix(sptUtil::mix(dirBegin, dirEnd, ratio)));
    transform.makeTranslate(sptUtil::mix(begin, end, ratio));

    return transform;

}; // Follower::getMatrix

void Follower::changeTrack(osg::Vec3 position)
{

    const Sector* sector = &(_track->getSector());
    osg::Vec3 offset(floor(position.x() / Sector::SIZE), floor(position.y() / Sector::SIZE), 0);

    // if position is outside current sector
    if(offset != osg::Vec3())
    {

        offset *= Sector::SIZE;
        sector = &(getScenery().getSector(sector->getPosition() + offset));
        position -= offset;

    };

    try
    {
        _track = &(sector->getNextTrack(position, *_track));
    }
    catch(Sector::UnknownConnectionException exc)
    {
        throw NullTrackException();
    };

    // if connection contained null track then sector is corrupt
    assert(_track != NULL);

    // update path
    _path = &(_track->getPath(position));

}; // Follower::moveToNextTrack
