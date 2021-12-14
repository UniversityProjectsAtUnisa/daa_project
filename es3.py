from .daa_collections.tree.linked_binary_tree import LinkedBinaryTree
from .daa_collections.map.map_base import MapBase


class MedianTreeMap(LinkedBinaryTree, MapBase):

    class _Node(LinkedBinaryTree._Node):
        # Added attribute _count to the node
        __slots__ = "_count"

        def __init__(self, element, parent=None, left=None, right=None):
            super().__init__(element, parent, left, right)
            self._count = 1

    class Position(LinkedBinaryTree.Position):
        def key(self):
            return self.element()._key

        def value(self):
            return self.element()._value

    def _subtree_search(self, p, k):
        if k == p.key():
            return p
        elif k < p.key():
            if self.left(p) is not None:
                return self._subtree_search(self.left(p), k)
        else:
            if self.right(p) is not None:
                return self._subtree_search(self.right(p), k)
        return p

    def _subtree_first_position(self, p):
        walk = p
        while self.left(walk) is not None:
            walk = self.left(walk)
        return walk

    def _subtree_last_position(self, p):
        walk = p
        while self.right(walk) is not None:
            walk = self.right(walk)
        return walk

    def first(self):
        return self._subtree_first_position(self.root()) if len(self) > 0 else None

    def last(self):
        return self._subtree_last_position(self.root()) if len(self) > 0 else None

    def before(self, p):
        self._validate(p)
        if self.left(p):
            return self._subtree_last_position(self.left(p))
        else:
            walk = p
            above = self.parent(walk)
            while above is not None and walk == self.left(above):
                walk = above
                above = self.parent(walk)
            return above

    def after(self, p):
        self._validate(p)
        if self.right(p):
            return self._subtree_first_position(self.right(p))
        else:
            walk = p
            above = self.parent(walk)
            while above is not None and walk == self.right(above):
                walk = above
                above = self.parent(walk)
            return above

    def find_position(self, k):
        if self.is_empty():
            return None
        else:
            p = self._subtree_search(self.root(), k)
            self._rebalance_access(p)
            return p

    def delete(self, p):
        self._validate(p)
        if self.left(p) and self.right(p):
            replacement = self._subtree_last_position(self.left(p))
            self._replace(p, replacement.element())
            p = replacement
        parent = self.parent(p)
        self._delete(p)
        self._rebalance_delete(parent)
        # Reducing _count of the nodes which are root of a subtree subject to the deletion
        self._fix_count_delete(parent)

    def __getitem__(self, k):
        if self.is_empty():
            raise KeyError('Key Error: ' + repr(k))
        else:
            p = self._subtree_search(self.root(), k)
            self._rebalance_access(p)
            if k != p.key():
                raise KeyError('Key Error: ' + repr(k))
            return p.value()

    def __setitem__(self, k, v):
        if self.is_empty():
            leaf = self._add_root(self._Item(k, v))
        else:
            p = self._subtree_search(self.root(), k)
            if p.key() == k:
                p.element()._value = v
                self._rebalance_access(p)
                return
            else:
                item = self._Item(k, v)
                if p.key() < k:
                    leaf = self._add_right(p, item)
                else:
                    leaf = self._add_left(p, item)
        self._rebalance_insert(leaf)
        # Increasing _count of the nodes which are root of a subtree subject to the insertion
        self._fix_count_insert(leaf)

    def __delitem__(self, k):
        if not self.is_empty():
            p = self._subtree_search(self.root(), k)
            if k == p.key():
                self.delete(p)
                return
            self._rebalance_access(p)
        raise KeyError('Key Error: ' + repr(k))

    def __iter__(self):
        p = self.first()
        while p is not None:
            yield p.key()
            p = self.after(p)

    def __reversed__(self):
        p = self.last()
        while p is not None:
            yield p.key()
            p = self.before(p)

    def find_min(self):
        if self.is_empty():
            return None
        else:
            p = self.first()
            return (p.key(), p.value())

    def find_max(self):
        if self.is_empty():
            return None
        else:
            p = self.last()
            return (p.key(), p.value())

    def find_le(self, k):
        if self.is_empty():
            return None
        else:
            p = self.find_position(k)
            if k < p.key():
                p = self.before(p)
            return (p.key(), p.value()) if p is not None else None

    def find_lt(self, k):
        if self.is_empty():
            return None
        else:
            p = self.find_position(k)
            if not p.key() < k:
                p = self.before(p)
            return (p.key(), p.value()) if p is not None else None

    def find_ge(self, k):
        if self.is_empty():
            return None
        else:
            p = self.find_position(k)
            if p.key() < k:
                p = self.after(p)
            return (p.key(), p.value()) if p is not None else None

    def find_gt(self, k):
        if self.is_empty():
            return None
        else:
            p = self.find_position(k)
            if not k < p.key():
                p = self.after(p)
            return (p.key(), p.value()) if p is not None else None

    def find_range(self, start, stop):
        if not self.is_empty():
            if start is None:
                p = self.first()
            else:
                p = self.find_position(start)
                if p.key() < start:
                    p = self.after(p)
            while p is not None and (stop is None or p.key() < stop):
                yield (p.key(), p.value())
                p = self.after(p)

    def _rebalance_insert(self, p):
        pass

    def _rebalance_delete(self, p):
        pass

    def _rebalance_access(self, p):
        pass

    def _relink(self, parent, child, make_left_child):
        if make_left_child:
            parent._left = child
        else:
            parent._right = child
        if child is not None:
            child._parent = parent

    def _rotate(self, p):
        x = p._node
        y = x._parent
        z = y._parent
        if z is None:
            self._root = x
            x._parent = None
        else:
            self._relink(z, x, y == z._left)
        if x == y._left:
            self._relink(y, x._right, True)
            self._relink(x, y, False)
        else:
            self._relink(y, x._left, False)
            self._relink(x, y, True)

    def _restructure(self, x):
        y = self.parent(x)
        z = self.parent(y)
        if (x == self.right(y)) == (y == self.right(z)):
            self._rotate(y)
            return y
        else:
            self._rotate(x)
            self._rotate(x)
            return x

    # ------------------------------------ NEW METHODS -------------------------------

    def _fix_count_insert(self, p):
        """Increases _count of the nodes which are root of a subtree subject to the insertion

        Args:
            p (Position): Position object that refers to the inserted node
        """
        self._validate(p)
        walk = self.parent(p)
        while walk:
            self._increase_count(walk)
            walk = self.parent(walk)

    def _fix_count_delete(self, p):
        """Reduces _count of the nodes which are root of a subtree subject to the deletion

        Args:
            p (Position): Position object that refers to the parent of the deleted node
        """
        if not p:
            # happens when the tree is empty
            return
        self._validate(p)
        walk = p
        while walk:
            self._decrease_count(walk)
            walk = self.parent(walk)

    def _increase_count(self, p):
        """Increases by one the _count of the node refered by the position given as input

        Args:
            p (Position): Position object that refers to a node of which the _count must be increased 
        """
        node = self._validate(p)
        node._count += 1

    def _decrease_count(self, p):
        """Decreases by one the _count of the node refered by the position given as input

        Args:
            p (Position): Position object that refers to a node of which the _count must be decreased 
        """
        node = self._validate(p)
        node._count -= 1

    def count(self, p):
        """Returns the _count of the node refered by the position given as input

        Args:
            p (Position): Position object that refers to a node of which the _count must be returned 

        Returns:
            int: the _count of the node refered by the position object in input
        """
        node = self._validate(p)
        return node._count

    def kth_smallest(self, p, k):
        """Returns the Position object that refers to a node 
        of which the element has a key that is 
        the kth smallest element in the key set.

        The key set considered is associated to the subtree 
        that starts from the node referred by the position object in input

        Args:
            p (Position): Position object that refers to the node which is root of the subtree
            k (int): the index of the key in an immaginary ordered list of keys from the key set

        Returns:
            Position: The position object associated to the kth smallest key in the key set
        """
        self._validate(p)
        count = 1
        left = self.left(p)
        if left:
            count += self.count(left)
        if k == count-1:
            return p
        if k < count-1:
            return self.kth_smallest(left, k)
        return self.kth_smallest(self.right(p), k-count)

    def median(self):
        """Returns a Position object that refers to a node 
        of which the element has a key that is
        the median element of the key set of the tree.
        
        Returns None if the tree is empty

        Returns:
            Position: The position object
        """
        n = len(self)
        if n == 0:
            return None
        m = n // 2
        return self.kth_smallest(self.root(), m)
