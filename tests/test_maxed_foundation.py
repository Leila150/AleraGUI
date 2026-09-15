from aleragui import *

def test_advanced_geometry():
    a=Vec2(0,0); b=Vec2(10,0)
    assert distance(a,b)==10
    assert Affine2D.translation(5,6).apply(a)==Vec2(5,6)
    assert Circle2D(Vec2(),5).contains(Vec2(3,4))

def test_render_graph():
    graph=RenderGraph(); p=graph.add_pass('main'); p.add(('rect',))
    assert len(graph.passes)==1 and len(p.commands)==1
    assert RendererFeatures(gpu=True).supports('gpu')

def test_input():
    manager=InputManager(); seen=[]
    manager.on('click',lambda e:seen.append(e.type))
    manager.dispatch(InputEvent(DeviceKind.MOUSE,'click'))
    assert seen==['click']

def test_theme():
    theme=DARK_PRO.derive('custom'); theme.cascade.add('Button',opacity=.5)
    button=Button(text='x'); button.style_class='foo'
    assert theme.style(button)['opacity']==.5

def test_catalog():
    assert WIDGET_COUNT >= 1000
    assert get_widget('PrimaryButton')

def test_properties():
    class Demo(Widget):
        value=AdvancedProperty(0,validator=number(0,10))
    d=Demo(); d.value=5
    assert d.value==5
