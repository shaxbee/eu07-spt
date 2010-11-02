"""
Test module for testing sptial library.
"""

import unittest

import sptial


class RTreeTest(unittest.TestCase):

    def testRootOnly(self):
        """
        Tests of insert and delete in root node of RTree.
        """
        
        tree = sptial.RTree(minSize = 1, pageSize = 3)
        tree.insert(sptial.Cuboid((-1, -1, -1), (1, 1, 1)), 'a')
        tree.insert(sptial.Cuboid((-2, -3, 9), (9, -2, 1)), 'b')
        tree.insert(sptial.Cuboid((1, -1, -1), (2, 1, 1)), 'c')
        
        self.assertEquals(3, len(tree))
        self.assertEquals(1, tree.level())

        self.assertTrue('a' in tree.query(sptial.Cuboid((-1, -1, -1), (2, 2, 2))))
        self.assertTrue('c' in tree.query(sptial.Cuboid((-1, -1, -1), (2, 2, 2))))
        self.assertFalse('b' in tree.query(sptial.Cuboid((-1, -1, -1), (2, 2, 2))))

        tree.delete(sptial.Cuboid((-1, -1, -1), (1, 1, 1)), 'a')
        tree.delete(sptial.Cuboid((-2, -3, 0), (9, -2, 1)), 'b')
        tree.delete(sptial.Cuboid((1, -1, -1), (2, 1, 1)), 'c')

        self.assertEquals(0, len(tree))


    def testFive(self):
        """
        Tests of insert and delete of five elements.
        The level of tree should be at most 3.
        """
        
        tree = sptial.RTree(minSize = 1, pageSize = 2)
        tree.insert(sptial.Cuboid((-1, -1, -1), (1, 1, 1)), 'a')
        tree.insert(sptial.Cuboid((-2, -3, 0), (9, -2, 1)), 'b')
        tree.insert(sptial.Cuboid((1, -1, -1), (2, 1, 1)), 'c')
        tree.insert(sptial.Cuboid((1, -1, -1), (20, 1, 1)), 'd')
        tree.insert(sptial.Cuboid((1, -1, -1), (2, 1, 10)), 'e')
        tree.checkParents()
    
        self.assertEquals(5, len(tree))
        self.assertEquals(3, tree.level())

        cq = sptial.Cuboid((-1, -1, -1), (2, 2, 2))
        self.assertTrue('a' in tree.query(cq))
        self.assertTrue('c' in tree.query(cq))
        self.assertFalse('b' in tree.query(cq))

        tree.delete(sptial.Cuboid((-1, -1, -1), (1, 1, 1)), 'a')
        tree.delete(sptial.Cuboid((-2, -3, 0), (9, -2, 1)), 'b')
        tree.delete(sptial.Cuboid((1, -1, -1), (2, 1, 1)), 'c')
        tree.checkParents()

        self.assertEquals(2, len(tree))


    def testSeven(self):
        """
        Tests the RTree with larger page size.
        Configuration mineSiz=1, pageSize=3
        """

        tree = sptial.RTree(minSize = 1, pageSize = 3)
        tree.insert(sptial.Cuboid((-1, 0, -1), (0, 1, 1)), 'a')
        tree.insert(sptial.Cuboid((-6, 8, 10), (-5, 10, 100)), 'b')
        tree.insert(sptial.Cuboid((-7, 6, 10), (-4, 9, 20)), 'c')
        tree.insert(sptial.Cuboid((3, 9, 87), (4, 10, 99)), 'd')
        tree.insert(sptial.Cuboid((-5, -7, -8), (1, 1, -4)), 'e')
        tree.insert(sptial.Cuboid((-9, -24, 40), (3, -8, 50)), 'f')
        tree.insert(sptial.Cuboid((-15, -1, 0), (12, 0, 1)), 'g')
        tree.checkParents()

        self.assertEquals(7, len(tree))
        self.assertEquals(2, tree.level())

        l = list(tree.query(sptial.Cuboid((-2, -1, -2), (1, 2, 1))))
        self.assertEquals(2, len(l))
        self.assertTrue('a' in l)
        self.assertTrue('g' in l)

        l = list(tree.query(sptial.Cuboid((-1, -1, 0), (0, 0, 1))))
        self.assertEquals(2, len(l))
        self.assertTrue('a' in l)
        self.assertTrue('g' in l)

        tree.delete(sptial.Cuboid((-7, 6, 10), (-4, 9, 20)), 'c')
        tree.checkParents()

        self.assertEquals(6, len(tree))

        tree.delete(sptial.Cuboid((-9, -24, 40), (3, -8, 50)), 'f')
        tree.delete(sptial.Cuboid((3, 9, 87), (4, 10, 99)), 'd')
        tree.delete(sptial.Cuboid((-6, 8, 99), (-5, 10, 100)), 'b')
        tree.checkParents()

        self.assertEquals(3, len(tree))
        self.assertEquals(1, tree.level())




if __name__ == "__main__":
     unittest.main()

