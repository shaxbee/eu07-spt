"""
SPaTial indexing structures.
"""

import decimal


class Cuboid:
    """
    Cuboid that is based on integer coordinates
    """

    def __init__(self, minX, maxX, minY, maxY, minZ, maxZ):
        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY
        self.minZ = minZ
        self.maxZ = maxZ


    def __repr__(self):
        return "(%d, %d, %d), (%d, %d, %d)" % \
            (self.minX, self.minY, self.minZ, self.maxX, self.maxY, self.maxZ)


    def __eq__(self, o):
        return self.minX == o.minX \
            and self.maxX == o.maxX \
            and self.minY == o.minY \
            and self.maxY == o.maxY \
            and self.minZ == o.minZ \
            and self.maxZ == o.maxZ


    def volume(self):
        """
        Returns the volume of the cuboid.

        Examples:
        >>> NullCuboid.volume()
        0
        >>> Cuboid(1, 2, -2, -1, -1, 1).volume()
        2
        """
        w = self.maxX - self.minX
        h = self.maxY - self.minY
        d = self.maxZ - self.minZ
        return w * h * d


    def overlap(self, oc):
        """
        Returns the volume of overlapping part of
        this cuboid and another.

        Examples:
        >>> c = Cuboid(0, 2, 0, 2, 0, 2)
        >>> c.overlap(NullCuboid)
        0
        >>> c.overlap(Cuboid(2, 3, -1, 0, 2, 4))
        0
        >>> c.overlap(Cuboid(-1, 1, 1, 3, 0, 2))
        2
        """
        return self.intersection(oc).volume()


    def contains(self, oc):
        return self.containsPoint(oc.minX, oc.minY, oc.minZ) \
            and self.containsPoint(oc.maxX, oc.maxY, oc.maxZ)


    def containsPoint(self, x, y, z):
        """
        Returns True if this contains the point.

        Examples:
        >>> c = Cuboid(-1, 2, -1, 2, 0, 3)
        >>> c.containsPoint(0, 0, 0)
        True
        >>> c.containsPoint(-1, -1, 0)
        True
        >>> c.containsPoint(-1, -1, -1)
        False
        >>> c.containsPoint(-2, -2, 4)
        False
        """
        return x >= self.minX and x <= self.maxX \
            and y >= self.minY and y <= self.maxY \
            and z >= self.minZ and z <= self.maxZ


    def intersects(self, oc):
        """
        Returns true if oc intersects this cuboid.

        Examples:
        >>> a = Cuboid(-1, 2, 0, 0, -2, 1)
        >>> b = Cuboid(-1, 2, 0, 0, -3, 1)
        >>> c = Cuboid(-1, 2, 0, 1, -2, 1)
        >>> d = Cuboid(-1, 2, -1, 0, -2, 1)        
        >>> a.intersects(b)
        True
        >>> c.intersects(a)
        True
        >>> a.intersects(d)
        True
        >>> c.intersects(d)
        True
        """
        if self == oc:
            return True
        inter = self.intersection(oc)
        if inter.volume() > 0:
            return True
        elif inter != NullCuboid:
            return True
        else:
            return False


    def intersection(self, oc):
        """
        Makes the intersection with given oc.

        Examples:
        >>> a = Cuboid(-1, 2, -2, 0, 1, 3)
        >>> b = Cuboid(0, 1, -1, 0, 2, 3)
        >>> c = Cuboid(-2, 0, -3, -1, 2, 4)
        >>> d = Cuboid(9, 10, 9, 10, 9, 10)
        >>> a.intersection(d)
        (0, 0, 0), (0, 0, 0)
        >>> a.intersection(b)
        (0, -1, 2), (1, 0, 3)
        >>> a.intersection(c)
        (-1, -2, 2), (0, -1, 3)
        """
        if self is NullCuboid: return NullCuboid
        if oc is NullCuboid: return NullCuboid

        minX, maxX = max(self.minX, oc.minX), min(self.maxX, oc.maxX)
        minY, maxY = max(self.minY, oc.minY), min(self.maxY, oc.maxY)
        minZ, maxZ = max(self.minZ, oc.minZ), min(self.maxZ, oc.maxZ)

        w, h, d = maxX - minX, maxY - minY, maxZ - minZ
        if w < 0 or h < 0 or d < 0: return NullCuboid
        if w == 0 and h == 0 and d == 0: return NullCuboid

        c = Cuboid(minX, maxX, minY, maxY, minZ, maxZ)
        #print c
        return c 


    def union(self, oc):
        """
        Makes the union of this cuboid and another one and returns the union.

        Examples:
        >>> a = Cuboid(-1, 3, -3, 2, -2, 3)
        >>> b = Cuboid(0, 1, 0, 1, 0, 1)
        >>> a.union(b) == a
        True
        >>> c = Cuboid(9, 10, 9, 10, -10, -9)
        >>> b.union(c)
        (0, 0, -10), (10, 10, 1)
        """
        if oc is NullCuboid: return Cuboid(self.minX, self.maxX, self.minY, self.maxY, self.minZ, self.maxZ)
        if self is NullCuboid: return Cuboid(oc.minX, oc.maxX, oc.minY, oc.maxY, oc.minZ, oc.maxZ)

        nMinX = self.minX if self.minX < oc.minX else oc.minX
        nMaxX = self.maxX if self.maxX > oc.maxX else oc.maxX
        nMinY = self.minY if self.minY < oc.minY else oc.minY
        nMaxY = self.maxY if self.maxY > oc.maxY else oc.maxY
        nMinZ = self.minZ if self.minZ < oc.minZ else oc.minZ
        nMaxZ = self.maxZ if self.maxZ > oc.maxZ else oc.maxZ

        return Cuboid(nMinX, nMaxX, nMinY, nMaxY, nMinZ, nMaxZ)


    def unionPoint(self, x, y, z):
        return self.union(Cuboid(x, x, y, y, z, z))
        

    @classmethod
    def fromEndpoints(cls, endpoints):
        """
        Transforms the endpoints = a sequence of Vec3 points.

        Examples:
        >>> from sptmath import Vec3
        >>> l = [Vec3('-0.551', '-1.000', '-1.001'), Vec3('2.000', '3.999', '32.090'), Vec3('0.000', '4.001', '4.000')]
        >>> Cuboid.fromEndpoints(l)
        (-1, -1, -2), (2, 5, 33)
        """
        xa = [p.x for p in endpoints]
        ya = [p.y for p in endpoints]
        za = [p.z for p in endpoints]
        
        minX = int(min(xa).to_integral_value(decimal.ROUND_FLOOR))
        maxX = int(max(xa).to_integral_value(decimal.ROUND_CEILING))
        minY = int(min(ya).to_integral_value(decimal.ROUND_FLOOR))
        maxY = int(max(ya).to_integral_value(decimal.ROUND_CEILING))
        minZ = int(min(za).to_integral_value(decimal.ROUND_FLOOR))
        maxZ = int(max(za).to_integral_value(decimal.ROUND_CEILING))

        return Cuboid(minX, maxX, minY, maxY, minZ, maxZ)


    @classmethod
    def unionAll(cls, seq):
        r = NullCuboid
        for k in seq:
            r = r.union(k)
        return r


NullCuboid = Cuboid(0, 0, 0, 0, 0, 0)


class RTree:
    """
    RTree implementation based on Cuboids with integral coordinates.
    """

    class LeafEntry:
        """
        A leaf entry contains cuboid and the object.
        """

        def __init__(self, cuboid, obj):
            self.cuboid = cuboid
            self.obj = obj


        def __repr__(self):
            return "Leaf: %s %s" % (self.cuboid, self.obj)


    class IndexEntry:
        """
        An index entry contains cuboid and the index to next Node.
        """

        def __init__(self, cuboid, index):
            self.cuboid = cuboid
            self.index = index


        def __repr__(self):
            return "Index: %s" % (self.cuboid)


    class Node:
        """
        Node contains children of either LeafEntries or IndexEntries.
        It contains at least RTree.minSize to RTree.pageSize at most entries.
        It has also the parent unless a tree root.
        """

        def __init__(self, parent = None, firstElem = None):
            self.children = []
            if firstElem is not None:
                self.addChild(firstElem)
            self.parent = parent
            

        def isLeaf(self):
            if len(self.children) > 0:
                return isinstance(self.children[0], RTree.LeafEntry)
            else:
                return self.isRoot()


        def isRoot(self): 
            return self.parent is None


        def cuboids(self):
            return [x.cuboid for x in self.children]


        def mbc(self):
            """
            Returns minimal bounding cuboid for this node.
            """
            return Cuboid.unionAll(self.cuboids())


        def findEntry(self, subnode):
            """
            Finds the entry of the subnode.
            """
            for c in self.children:
                if c.index is subnode:
                    return c
            return None


        def __repr__(self):
            return "parent: [%s] children: %s" % (self.parent, self.children)


        def addChild(self, entry):
            self.children.append(entry)
            if isinstance(entry, RTree.IndexEntry):
                entry.index.parent = self
        

        def addChildren(self, entries):
            for e in entries:
                self.addChild(e)


    def __init__(self, pageSize = 20, minSize = 10):
        self.__size = 0
        self.__level = 1
        self.__pageSize = pageSize
        self.__minSize = minSize
        self.__root = self.Node()


    def insert(self, cuboid, obj):
        """
        Inserts a new index entry.

        Example:
        >>> rtree = RTree()
        >>> len(rtree)
        0
        >>> from sptmath import Vec3
        >>> l = [Vec3('-0.551', '-1.000', '-1.001'), Vec3('2.000', '3.999', '32.090'), Vec3('0.000', '4.001', '4.000')] 
        >>> cub1 = Cuboid.fromEndpoints(l)
        >>> rtree.insert(cub1, 'a')
        >>> len(rtree)
        1
        >>> rtree.level()
        1
        """
        # choose leaf
        node = self.chooseLeaf(self.__root, cuboid)
        splitNode = None
        newEntry = self.LeafEntry(cuboid, obj)
        self.__size += 1
        if len(node.children) < self.__pageSize:
            # install E
            node.children.append(newEntry)
        else:
            # split node
            node, splitNode = self.splitNode(node, newEntry)
        # adjust tree
        node, splitNode = self.adjustTree(node, splitNode)
        # if node split propagation caused root to split
        if splitNode is not None:
            root = self.Node()
            root.addChild(self.IndexEntry(node.mbc(), node))
            root.addChild(self.IndexEntry(splitNode.mbc(), splitNode))
            self.__level += 1
            self.__root = root
            
        


    def chooseLeaf(self, node, cuboid):
        """
        Select a leaf node in which to place a new LeafEntry.
        """
        if node.isLeaf():
            return node
        else:
            child = None
            minVol = -1
            for c in node.children:
                v = c.cuboid.union(cuboid).volume() - c.cuboid.volume()
                if minVol < 0 or v < minVol:
                    minVol = v
                    child = c.index

            return self.chooseLeaf(child, cuboid)
    

    def splitNode(self, node, newElem):
        """
        Divide a set of M+1 entries into two groups.
        """
        entries = node.children + [newElem]
        s1, s2 = self.pickSeeds(entries)
        #ga = self.Node(node.parent, s1)
        ga = node
        ga.children = []
        ga.addChild(s1)
        gb = self.Node(node.parent, s2)
        while len(entries) > 0:
            # 3.5.2. if one group has so few entries...
            #if self.__pageSize + 1 - len(ga.children) == self.__minSize:
            if self.__pageSize - len(ga.children) == self.__minSize:
                ga.addChildren(entries)
                break
            #elif self.__pageSize + 1 - len(gb.children) == self.__minSize:
            elif self.__pageSize - len(gb.children) == self.__minSize:
                gb.addChildren(entries)
                break

            e = self.pickNext(ga, gb, entries)
            da = ga.mbc().union(e.cuboid).volume() - ga.mbc().volume()
            db = gb.mbc().union(e.cuboid).volume() - gb.mbc().volume()
            if da < db:
                ga.addChild(e)
            elif da > db:
                gb.addChild(e)
            else:
                if len(ga.children) < len(gb.children):
                    ga.addChild(e)
                else:
                    gb.addChild(e)
            entries.remove(e)
        return (ga, gb)


    def pickSeeds(self, entries):
        """
        Selects two entries to be the first elements of the groups.
        Quadratic Cost algorithm
        """
        worst = -1
        seedA = None
        seedB = None
        elen = len(entries)
        for i in range(0, elen):
            for j in range(i+1, elen):
                e1 = entries[i]
                e2 = entries[j]
                jc = e1.cuboid.union(e2.cuboid)
                d = jc.volume() - e1.cuboid.volume() - e2.cuboid.volume()
                if d > worst:
                    worst = d
                    seedA = e1
                    seedB = e2
        entries.remove(seedA)
        entries.remove(seedB)
        return (seedA, seedB)


    def pickNext(self, groupA, groupB, entries):
        """
        Select one remaining entry for a classification in a group.
        """
        diff = -1 
        next = None
        for e in entries:
            d1 = groupA.mbc().union(e.cuboid).volume() - groupA.mbc().volume()
            d2 = groupB.mbc().union(e.cuboid).volume() - groupB.mbc().volume()
            if abs(d1-d2) > diff:
                diff = abs(d1-d2)
                next = e
        return next

        
    def adjustTree(self, node, splitNode):
        """
        Ascend from a leaf node to the root, adjusting covering
        cubics and propagating node splits as necessary.
        """
        while not node.isRoot():
            parent = node.parent
            subEntry = parent.findEntry(node)
            assert subEntry is not None, node
            subEntry.cuboid = node.mbc()
            if splitNode is not None:
                nnEntry = self.IndexEntry(splitNode.mbc(), splitNode)
                if len(parent.children) < self.__pageSize:
                    parent.addChild(nnEntry)
                    splitNode = None
                else:
                    # split node
                    node, splitNode = self.splitNode(parent, nnEntry)
            #else:
            #    node = parent
            node = parent
        return node, splitNode
        
        

    def delete(self, cuboid, obj):
        """
        Remove object from rtree.

        Examples:
        >>> rtree = RTree(minSize = 1, pageSize = 2)
        >>> len(rtree)
        0
        >>> from sptmath import Vec3
        >>> l = [Vec3('-0.551', '-1.000', '-1.001'), Vec3('2.000', '3.999', '32.090'), Vec3('0.000', '4.001', '4.000')] 
        >>> cub1 = Cuboid.fromEndpoints(l)
        >>> rtree.insert(cub1, 'a')
        >>> rtree.insert(Cuboid(1, 2, 1, 2, 1, 2), 'b')
        >>> rtree.insert(Cuboid(3, 4, 3, 4, 3, 4), 'c')
        >>> len(rtree)
        3
        >>> rtree.delete(Cuboid(1, 2, 1, 2, 1, 2), 'b')
        True
        >>> len(rtree)
        2
        >>> list(iter(rtree))
        ['a', 'c']
        """
        deleted = False
        leafNode = self.findLeaf(self.__root, obj, cuboid)
        if leafNode is None:
            return False # nothing was removed
        dindex = -1
        for c in leafNode.children:
            dindex += 1
            if c.obj == obj:
                break
        if dindex > -1:
            del leafNode.children[dindex]
            self.__size -= 1
            deleted = True
        self.condenseTree(leafNode)
        # reassign root
        if len(self.__root.children) == 1 and self.__size > 1:
            self.__root = self.__root.children[0].index
            self.__root.parent = None
            self.__level -= 1
        return deleted


    def findLeaf(self, node, o, cuboid):
        """
        Find the leaf containing entry
        """
        if not node.isLeaf():
            for c in node.children:
                if c.cuboid.intersects(cuboid):
                    leafNode = self.findLeaf(c.index, o, cuboid)
                    if leafNode is not None:
                        return leafNode
        else:
            for c in node.children:
                if c.obj == o:
                    return node
        return None


    def condenseTree(self, node):
        """
        Given a leaf from which an entry has been deleted,
        eliminate the node if it has too few entries and relocate
        its entries. Propagate node elimination upward as necessary.
        Adjust all ocvering cuboids on the path to the root, make
        them smaller if possible.
        """
        toEliminate = []
        parent = node.parent
        while parent is not None:
            subEntry = parent.findEntry(node)
            assert subEntry is not None, node
            if len(node.children) < self.__minSize:
                parent.children.remove(subEntry)
                toEliminate.append(node)
            else:
                subEntry.cuboid = node.mbc()
            node = parent
            parent = node.parent
        # reinsert orphaned entries
        for n in toEliminate:
            for ins in self.iterateOverLeaves(n):
                self.insert(ins.cuboid, ins.obj)


    def query(self, cuboid):
        """
        Find all records whose cuboids overlap a search cuboid.

        Example:
        >>> rtree = RTree()
        >>> rtree.insert(Cuboid(-6, 7, 9, 14, 13, 14), 'bbb')
        >>> list(rtree.query(Cuboid(-99, -98, -98, -7, 6, 7)))
        []
        >>> list(rtree.query(Cuboid(0, 1, 10, 11, 13, 14)))
        ['bbb']
        """
        def p(o): return cuboid.intersects(o.cuboid)
        return self._query(self.__root, p)


    def _query(self, node, pred):
        if not node.isLeaf():
            for c in node.children:
                if pred(c):
                    for s in self._query(c.index, pred):
                        yield s
        else:
            for c in node.children:
                if pred(c):
                    yield c.obj
                     


    def queryPoint(self, x, y, z):
        """
        Queries for the point.

        Examples:
        >>> rtree = RTree()
        >>> rtree.insert(Cuboid(-6, 7, 9, 14, 13, 14), 'bbb')
        >>> list(rtree.queryPoint(-99, -98, -98))
        []
        >>> list(rtree.queryPoint(2, 14, 13))
        ['bbb']
        """
        def p(o): return o.cuboid.containsPoint(x, y, z)
        return self._query(self.__root, p)


    def __len__(self):
        return self.__size


    def level(self):
        return self.__level


    def __iter__(self):
        """
        Iterates over leaf objects in RTree.
        """
        for l in self.iterateOverLeaves(self.__root):
            yield l.obj
        

    def iterateOverLeaves(self, node):
        if node.isLeaf():
            for c in node.children:
                yield c
        else:
            for c in node.children:
                for x in self.iterateOverLeaves(c.index):
                    yield x


    def __repr__(self):
        s = "Root: %s\nLeaves: " % self.__root.children
        for l in self.iterateOverLeaves(self.__root):
            s += str(l) + ", "
        return s


    def str(self):
        s = "["
        for l in self:
            s += str(l) + ", "
        s += "]"
        return s


    def checkParents(self):
        """
        Sanity check for parents of nodes.
        """
        self._checkParents(self.__root)
        

    def _checkParents(self, node):
        if not node.isLeaf():
            for c in node.children:
                assert c.index.parent is node, (c.index, node)
                self._checkParents(c.index)


    def getRoot(self):
        return self.__root

