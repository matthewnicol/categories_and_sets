import unittest

from pycats import CategorySet, CategoryItem, Traversal


class TestCategoryItem(unittest.TestCase):

    def test_auto_set(self):
        """
        Does [CategoryItem.set()] give us the [Item]Set class?
        """
        class Folder(CategoryItem):
            items = Traversal('FileSet')

        Folder.derivation(
            ['filesystem'],
            lambda x: [f"/home/{x['filesystem']}/files"]
        )

        FolderSet = Folder.set()
        self.assertEqual(FolderSet.__name__, 'FolderSet')


    def test_basic_derivation(self):
        """
        Does a hardcoded derivation show up when we try to traverse to it with an appropriate context
        """
        class Folder(CategoryItem):
            items = Traversal('FileSet')

        Folder.derivation(
            ['filesystem'],
            lambda x: [f"/home/{x['filesystem']}/files"]
        )

        FolderSet = Folder.set()
        self.assertEqual(FolderSet(filesystem='ourfs').items, ['/home/ourfs/files'])

    def test_basic_traversal(self):
        class Folder(CategoryItem):
            my_files = Traversal('FileSet')

        Folder.derivation(
            ['filesystem'],
            lambda x: [f"/home/{x['filesystem']}/files"]
        )

        class File(CategoryItem):
            pass

        File.derivation(None, lambda x: [])

        FileSet = File.set()
        FolderSet = Folder.set()

        f = Folder('testing')
        self.assertEqual(f.my_files, FileSet(items=[]))



