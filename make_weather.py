import bpy, math, random, os
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
def mat(name,color,metal=0,rough=.4):
 m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True; p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough;return m
cloudmat=mat('Pearlescent cloud',(.72,.83,.94),.12,.32);sunmat=mat('Warm sunlight',(1,.65,.19),.12,.32);rainmat=mat('Blue glass rain',(.24,.62,.88),.4,.16)
def sphere(name,loc,scale,material):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=40,ring_count=24,location=loc);o=bpy.context.object;o.name=name;o.scale=scale; o.data.materials.append(material)
 for p in o.data.polygons:p.use_smooth=True
 return o
# Blender Z-up exports to glTF Y-up.
for i,(x,y,z,sx,sy,sz) in enumerate([(-1.1,0,.05,.8,.65,.63),(-.45,0,.48,.91,.75,.95),(.45,.1,.58,.82,.72,.85),(1.12,0,.1,.77,.62,.59),(0,-.25,-.02,1.12,.69,.55)]):sphere('Cloud_'+str(i),(x,y,z),(sx,sy,sz),cloudmat)
sphere('Sun',(.92,.65,1.17),(.83,.28,.83),sunmat)
random.seed(17)
for i in range(28):
 x=random.uniform(-1.45,1.45);z=random.uniform(-2.15,-.7);y=random.uniform(-.2,.6)
 o=sphere('Rain_'+str(i),(x,y,z),(.024,.024,random.uniform(.08,.15)),rainmat);o.rotation_euler[1]=-.2
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath('weather.blend'))
bpy.ops.export_scene.gltf(filepath=os.path.abspath('dist/assets/weather.glb'),export_format='GLB',export_yup=True)
