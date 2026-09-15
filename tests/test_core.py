import unittest
from aleragui import Button, Label, CustomLayout, Canvas, Vec2, Bounds, point_in_polygon, Easing

class CoreTests(unittest.TestCase):
    def test_button_content_exclusive(self):
        with self.assertRaises(ValueError): Button()
        with self.assertRaises(ValueError): Button(text="x", image="x.png")
        self.assertIsInstance(Button(text="x"), Button)
    def test_reactive_invalidation(self):
        label=Label("hello"); label.validate(); label.text="world"; self.assertTrue(label.invalidated)
    def test_custom_layout(self):
        layout=CustomLayout(); label=Label("x"); layout.add(label); label.position=(100,200); self.assertEqual(label.position,(100,200))
    def test_geometry(self):
        self.assertEqual(Vec2(1,2)+Vec2(3,4),Vec2(4,6)); self.assertTrue(Bounds(0,0,10,10).contains(Vec2(5,5)))
        self.assertTrue(point_in_polygon(Vec2(1,1),[Vec2(0,0),Vec2(2,0),Vec2(2,2),Vec2(0,2)]))
    def test_canvas_shapes(self):
        canvas=Canvas(); canvas.polygon([(0,0),(10,0),(5,10)]); self.assertTrue(canvas.layers)
    def test_easing(self):
        self.assertEqual(Easing.linear(0.5),0.5)

if __name__ == "__main__": unittest.main()
