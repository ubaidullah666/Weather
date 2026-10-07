import bpy, math, os
from mathutils import Vector
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=64;s.cycles.use_denoising=True;s.render.film_transparent=True;s.render.resolution_x=360;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.view_settings.view_transform='Standard'
s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.15,.15,.15,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.25
m=bpy.data.materials.new('Fine-grained blackened metal');m.use_nodes=True;n=m.node_tree.nodes;p=n.get('Principled BSDF');p.inputs['Base Color'].default_value=(.008,.008,.008,1);p.inputs['Metallic'].default_value=.22;p.inputs['Roughness'].default_value=.51
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=280;noise.inputs['Detail'].default_value=2;bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.24;bump.inputs['Distance'].default_value=.009;m.node_tree.links.new(noise.outputs['Fac'],bump.inputs['Height']);m.node_tree.links.new(bump.outputs['Normal'],p.inputs['Normal'])
bpy.ops.object.camera_add(location=(0,0,9));cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=3.24;s.camera=cam
for loc,energy,size,color in [((-3,4,6),370,3,(1,1,1)),((4,1,3),260,4,(1,1,1)),((0,2.8,2.2),400,1.3,(1,.005,.015))]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=energy;o.data.shape='DISK';o.data.size=size;o.data.color=color;o.rotation_euler=(-o.location).to_track_quat('-Z','Y').to_euler()
 if color[1]<.1:
  o.data.type='SPOT';o.data.energy=400;o.data.spot_size=.65;o.data.spot_blend=.7;o.rotation_euler=(Vector((0,1.4,0))-o.location).to_track_quat('-Z','Y').to_euler()
font=bpy.data.fonts.load(os.path.abspath('BebasNeue-Regular.ttf'))
for digit in os.environ.get('TEMPERATURE_DIGITS','0123456789-'):
 for o in list(s.objects):
  if o.type not in ['CAMERA','LIGHT']:bpy.data.objects.remove(o,do_unlink=True)
 bpy.ops.object.text_add();o=bpy.context.object;o.name='Sculpted temperature '+digit;o.data.body=digit;o.data.font=font;o.data.align_x='CENTER';o.data.align_y='CENTER';o.data.resolution_u=24;o.data.extrude=.08;o.data.bevel_depth=.035;o.data.bevel_resolution=0
 bpy.ops.object.convert(target='MESH');bpy.context.view_layer.update();o.dimensions=(.86 if digit not in '1-' else (.5 if digit=='1' else .55),3 if digit!='-' else .23,.28);bpy.context.view_layer.update();bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);bpy.ops.object.mode_set(mode='EDIT');bpy.ops.mesh.select_all(action='SELECT');bpy.ops.mesh.remove_doubles(threshold=.0001);bpy.ops.object.mode_set(mode='OBJECT')
 for face in o.data.polygons:face.use_smooth=False
 # Center true mesh bounds; all digits use the same cap height.
 vs=[v.co for v in o.data.vertices];center=Vector(tuple((min(v[k] for v in vs)+max(v[k] for v in vs))/2 for k in range(3)))
 for v in o.data.vertices:v.co-=center
 # The font curve supplies a single flat chamfer before mesh conversion.
 o.data.materials.append(m);o.rotation_euler=(0,-.09,0)
 s.render.filepath=os.path.abspath('dist/assets/sculptures/digit-'+('minus' if digit=='-' else digit)+'.png');bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath('temperature.blend'))
