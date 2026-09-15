import unittest

from aleragui import AleraGUI, Button, Container, Event, Label, WidgetTree, hit_test


class RuntimeTests(unittest.TestCase):
    def test_ids_are_unique_and_queryable(self):
        root=Container(id="root",size=(300,300))
        button=Button(id="save",text="Save",position=(10,10),size=(100,40),style_class="primary")
        label=Label("Hello",style_class="primary")
        root.add(button,label)
        tree=WidgetTree(root)
        self.assertIs(tree.get("save"),button)
        self.assertEqual(tree.query("#save"),[button])
        self.assertEqual(tree.query(".primary"),[button,label])
        ids=[node.id for node in tree.walk()]
        self.assertEqual(len(ids),len(set(ids)))

    def test_reactive_changes_invalidate(self):
        label=Label("A")
        changes=[]
        label.watch("text",lambda new,old: changes.append((old,new)))
        label.text="B"
        self.assertTrue(label.invalidated)
        self.assertEqual(changes,[('A','B')])

    def test_hit_testing(self):
        root=Container(id="root",position=(0,0),size=(300,300))
        button=Button(id="b",text="X",position=(20,30),size=(100,50))
        root.add(button)
        result=hit_test(root,(40,50))
        self.assertIsNotNone(result)
        self.assertIs(result.widget,button)
        self.assertEqual(result.local_position,(20,20))

    def test_event_bubbles(self):
        root=Container(id="root")
        child=Button(id="child",text="X")
        root.add(child)
        seen=[]
        root.on("click",lambda event: seen.append(event.current_target.id))
        child.click()
        child.dispatch(Event("click",source=child))
        self.assertEqual(seen,['root'])

    def test_page_collection(self):
        class App(AleraGUI):
            @AleraGUI.page(name="Home")
            def home(self):
                return Label("Home")
        app=App()
        self.assertIn("Home",app.pages)


if __name__ == "__main__":
    unittest.main()
