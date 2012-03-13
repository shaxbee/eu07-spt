#ifndef SPTCORE_TRACKVISITOR_H
#define SPTCORE_TRACKVISITOR_H 1

namespace sptCore
{

class SimpleTrack;
class Switch;

class TrackVisitor
{
public:
    virtual ~TrackVisitor();

    virtual void apply(const SimpleTrack& value) = 0;
    virtual void apply(const Switch& value) = 0;
}; // class sptCore::TrackVisitor

}; // namespace sptCore

#endif // headerguard
