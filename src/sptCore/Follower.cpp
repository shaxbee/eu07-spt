#include <sptCore/Follower.h>

#include <assert.h>

#include <sptUtil/Math.h>

#include <sptCore/Track.h>
#include <sptCore/Scenery.h>

using namespace sptCore;

namespace 
{

class FindPosition
{
public:
    FindPosition(const float& search, const osg::Vec3& front): _search(search), _position(0.0), _previous(front) { };

    bool operator()(const osg::Vec3f& point)
    {
        _current = point;
        _position += (_current - _previous).length();
        return _position < _search;
    };

    float getRatio() const
    {
        return (_position - _search) / (_current - _previous).length();
    };

    osg::Vec3f getPosition() const
    {
        float ratio = getRatio();
        return (_previous * ratio + _current * (1 - ratio));
    };

    const osg::Vec3f& getCurrent() const { return _current; };
    const osg::Vec3f& getPrevious() const { return _previous; };

private:
    float _search;
    float _position;

    osg::Vec3 _current;
    osg::Vec3 _previous;

};

}; // anonymous namespace

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

osg::Vec3 Follower::getPosition() const
{

    FindPosition finder(_distance, _path->front());
    osg::Vec3Array::const_iterator iter = std::find_if(_path->points()->begin() + 1, _path->points()->end(), finder);

    return finder.getPosition();

}; // Follower::getPosition

osg::Matrix Follower::getMatrix() const
{

    FindPosition finder(_distance, _path->front());
    osg::Vec3Array::const_iterator iter = std::find_if(_path->points()->begin() + 1, _path->points()->end(), finder);

    // for first segment direction is equal to begin control vector
    osg::Vec3 dirBegin;
    if(finder.getPrevious() == _path->front())
    {
        dirBegin = _path->frontDir();
    }
    else
    {
        dirBegin = finder.getCurrent() - finder.getPrevious();
        dirBegin.normalize();
    };

    // for last segment direction is equal to end control vector
    osg::Vec3 dirEnd;
    if(finder.getCurrent() == _path->back())
    {
        dirEnd = _path->backDir();
    }
    else
    {
        dirEnd = *(iter + 1) - finder.getCurrent();
        dirEnd.normalize();
    };

    // create rotation matrix for given direction vector
    osg::Matrix transform(sptUtil::rotationMatrix(sptUtil::mix(dirBegin, dirEnd, finder.getRatio())));
    transform.makeTranslate(finder.getPosition());

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
