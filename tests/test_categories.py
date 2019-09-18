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

        f = Folder('testing')
        self.assertEqual(f.my_files, FileSet(items=[]))

    def test_traversal_with_aliasing(self):
        class Folder(CategoryItem):
            sub_folders = Traversal('Folder', rename_this='parent_folder')

        Folder.derivation(
            ['parent_folder'],
            lambda x: [f"/{x['parent_folder']}/files", f"/{x['parent_folder']}/cache"]
        )

        x = Folder('test_folder')
        sf = x.sub_folders
        self.assertEqual(sf.context['parent_folder'], 'test_folder')

        self.assertEqual(sf.items, ['/test_folder/files', '/test_folder/cache'])

    def test_multiple_traversals(self):
        class Computer(CategoryItem):
            folders = Traversal('Folder')

        ComputerSet = Computer.set()

        class Folder(CategoryItem):
            files = Traversal('File')

        class File(CategoryItem):
            pass

        Computer.derivation(None, lambda x: ['home', 'work', 'library', 'school'])

        def folders(context):
            if context['computer'] == 'home':
                return ['Documents', 'Videos', 'Pictures', 'Memes']
            elif context['computer'] == 'work':
                return ['Documents', 'Emails']
            elif context['computer'] == 'library':
                return ['Catalogue', 'Archives', 'Journals']
            elif context['computer'] == 'school':
                return ['Projects', 'Documents', 'Lectures']

        Folder.derivation(['computer'], folders)

        def files(context):
            if context['computer'] == 'home' and context['folder'] == 'Documents':
                return ['homedoc1.xls', 'homedoc2.pdf']
            if context['computer'] == 'work' and context['folder'] == 'Documents':
                return ['workdoc1.xls', 'workdoc2.pdf']
            return []

        File.derivation(['computer', 'folder'], files)

        x = ComputerSet()
        self.assertEqual(x.items, ['home', 'work', 'library', 'school'])

        f = x('home').folders
        ff = f('Documents').files

        self.assertEqual(ff.context['computer'], 'home')
        self.assertEqual(ff.context['folder'], 'Documents')
        self.assertEqual(ff.items, ['homedoc1.xls', 'homedoc2.pdf'])

    def test_lookup_name_traversal(self):
        class Computer(CategoryItem):
            folders = Traversal('Folder', lookup_key='lookup_key')

        ComputerSet = Computer.set()

        def folder_lookup(context, k):
            if k == 'lookup_key':
                return [1,2,3,4]
            else:
                return [4,5,6,7]

        class Folder(CategoryItem):
            pass

        Folder.derivation(None, folder_lookup)

        self.assertEqual(Computer('bob').folders, Folder.set()(items=[1,2,3,4]))

    def test_item_to_item_traversal(self):
        class Player(CategoryItem):
            @property
            def opponent(self):
                return Player(
                    'black' if self.identity == 'white' else 'white',
                   **{**self.context, 'opponent': self.identity}
                )

        p = Player('white')
        op = p.opponent

        self.assertEqual(op.identity, 'black')
        self.assertEqual(op.opponent.identity, 'white')
        self.assertEqual(p, p.opponent.opponent)

    def test_set_logic(self):

        class Conference(CategoryItem):
            team = Traversal('team')

        Conference.derivation([], lambda x: ['eastern', 'western'])

        class Team(CategoryItem):
            pass

        def conf_team_list(context):
            if context['conference'] == 'eastern':
                return [
                    'bucks', 'raptors', '76ers', 'celtics',
                    'pacers', 'nets', 'magic', 'pistons',
                    'hornets', 'heat', 'wizards', 'hawks',
                    'bulls', 'cavaliers', 'knicks'
                ]
            if context['conference'] == 'western':
                return [
                    'warriors', 'nuggets', 'trailblazers', 'rockets',
                    'jazz', 'thunder', 'spurs', 'clippers', 'kings',
                    'lakers', 'timberwolves', 'grizzlies', 'pelicans',
                    'mavericks', 'suns'
                ]

        def state_team_list(context):
            if context['state'] == 'LA':
                return ['lakers', 'clippers', 'kings', 'warriors', 'suns']

        Team.derivation(['conference'], conf_team_list)
        Team.derivation(['state'], state_team_list)

        st = Team.set()
        la = st(state='LA')
        west = st(conference='western')

        la_and_west = (la & west)

        self.assertTrue(Team('lakers') in la_and_west)
        self.assertTrue(Team('clippers') in la_and_west)
        self.assertTrue(Team('warriors') in la_and_west)
        self.assertTrue(Team('kings') in la_and_west)
        self.assertTrue(Team('suns') in la_and_west)
        self.assertEqual(len(la_and_west), 5)

        t1 = st(items=['lakers', 'warriors'])
        t2 = st(items=['warriors', 'clippers'])

        t1_or_t2 = (t1 | t2)
        self.assertTrue(Team('lakers') in t1_or_t2)
        self.assertTrue(Team('clippers') in t1_or_t2)
        self.assertTrue(Team('warriors') in t1_or_t2)
        self.assertEqual(len(t1_or_t2), 3)

        t1_xor_t2 = (t1 ^ t2)
        self.assertTrue(Team('lakers') in la_and_west)
        self.assertTrue(Team('clippers') in la_and_west)









