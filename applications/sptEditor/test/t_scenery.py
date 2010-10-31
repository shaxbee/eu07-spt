"""
Test case for scenery.
"""

import unittest
import model.scenery
import model.tracks
import model.groups
from sptmath import Vec3
import yaml
import sptyaml
import sptial



class SceneryTest(unittest.TestCase):

    def testReadWrite(self):
        sceneryToWrite = model.scenery.Scenery()

        group1 = model.groups.RailContainer()
        group1.insert(model.tracks.Track(p1 = Vec3('26.250', '-51.250', '0.000'), \
            p2 = Vec3('28.880', '-45.857', '0.000') ))
        group1.insert(model.tracks.Switch(pc = Vec3('28.880', '-45.857', '0.000'), \
            p1 = Vec3('43.446', '-15.989', '0.000'), \
            p2 = Vec3('45.068', '-16.856', '0.000'), \
            vc2 = Vec3('4.856', '9.958', '0.000'), \
            v2 = Vec3('-5.928', '-9.361', '0.000')))

        group2 = model.groups.RailContainer()
        group2.insert(model.tracks.Track(p1 = Vec3('43.446', '-15.989', '0.000'), \
            v1 = Vec3('4.856', '9.958', '0.000'), \
            v2 = Vec3('-3.726', '-10.435', '0.000'), \
            p2 = Vec3('56.330', '14.623', '0.000')))
        group2.insert(model.tracks.Switch(pc = Vec3('69.214', '45.235', '0.000'), \
            p1 = Vec3('54.649', '15.368', '0.000'), \
            p2 = Vec3('56.330', '14.623', '0.000'), \
            vc2 = Vec3('-4.856', '-9.958', '0.000'), \
            v2 = Vec3('3.726', '10.435', '0.000')))

        track3 = model.tracks.Track(p1 = Vec3('44.395', '-3.000', '0.000'), \
            v1 = Vec3('3.755', '5.929', '0.000'), \
            v2 = Vec3('-3.076', '-6.307', '0.000'), \
            p2 = Vec3('54.649', '15.368', '0.000'))

        sceneryToWrite.AddRailTracking(group1)
        sceneryToWrite.AddRailTracking(group2)
        sceneryToWrite.AddRailTracking(track3)

        self.assertEquals(len(sceneryToWrite.tracks.children), 3)

        text = yaml.dump(sceneryToWrite)

        sceneryAfterRead = yaml.load(text, sptyaml.SptLoader)

        self.assertEquals(len(sceneryAfterRead.tracks.children), 3)

        l = list(sceneryAfterRead.tracks.children.query(sptial.Cuboid(26, 46, -52, -15, 0, 0)))
        ll = list(l[0].children)
        self.assertTrue( \
            model.tracks.Track( \
                p1 = Vec3('26.250', '-51.250', '0.000'), \
                p2 = Vec3('28.880', '-45.857', '0.000') ) in ll)
        self.assertTrue( \
            model.tracks.Switch( \
                pc = Vec3('28.880', '-45.857', '0.000'), \
                p1 = Vec3('43.446', '-15.989', '0.000'), \
                p2 = Vec3('45.068', '-16.856', '0.000'), \
                vc2 = Vec3('4.856', '9.958', '0.000'), \
                v2 = Vec3('-5.928', '-9.361', '0.000')) in ll)

        l = list(sceneryAfterRead.tracks.children.query(sptial.Cuboid(43, 70, -16, 46, 0, 0)))
        ll = list(l[1].children)
        self.assertTrue( \
            model.tracks.Track( \
                p1 = Vec3('43.446', '-15.989', '0.000'), \
                v1 = Vec3('4.856', '9.958', '0.000'), \
                v2 = Vec3('-3.726', '-10.435', '0.000'), \
                p2 = Vec3('56.330', '14.623', '0.000')) in ll)
        self.assertTrue( \
            model.tracks.Switch( \
                pc = Vec3('69.214', '45.235', '0.000'), \
                p1 = Vec3('54.649', '15.368', '0.000'), \
                p2 = Vec3('56.330', '14.623', '0.000'), \
                vc2 = Vec3('-4.856', '-9.958', '0.000'), \
                v2 = Vec3('3.726', '10.435', '0.000')) in ll)

        l = list(sceneryAfterRead.tracks.children.query(sptial.Cuboid(44, 55, -4, 16, 0, 0)))
        self.assertTrue( \
            model.tracks.Track( \
                p1 = Vec3('44.395', '-3.000', '0.000'), \
                v1 = Vec3('3.755', '5.929', '0.000'), \
                v2 = Vec3('-3.076', '-6.307', '0.000'), \
                p2 = Vec3('54.649', '15.368', '0.000')) in l)



if __name__ == '__main__':
     unittest.main()

