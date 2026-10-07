import bpy,math,random,os
from mathutils import Vector
OUT=os.path.abspath('dist/assets/sculptures');os.makedirs(OUT,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=24;sc.cycles.use_denoising=True;sc.render.film_transparent=True;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.resolution_percentage=100;sc.world.color=(.45,.45,.45);sc.view_settings.view_transform='Standard'
def material(name,color,rough=.45,noise=False):
 m=bpy.data.materials.new(name);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough;p.inputs['Metallic'].default_value=.16
 if noise:
  n=m.node_tree.nodes.new('ShaderNodeTexNoise');n.inputs['Scale'].default_value=170;n.inputs['Detail'].default_value=2;b=m.node_tree.nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=.19;b.inputs['Distance'].default_value=.003 if name.startswith('Charcoal') else .025;m.node_tree.links.new(n.outputs['Fac'],b.inputs['Height']);m.node_tree.links.new(b.outputs['Normal'],p.inputs['Normal'])
 return m
black=material('Charcoal sculpted metal',(.006,.006,.006),.36,True);red=material('Signal red',(.96,.002,.024),.6,True);white=material('Porcelain',(.78,.8,.8),.75,True)
bpy.ops.object.camera_add(location=(0,0,8));cam=bpy.context.object;cam.data.type='ORTHO';cam.data.ortho_scale=3.5;sc.camera=cam
lights=[]
for loc,power,size in [((-3,4,6),650,4),((4,1,2),220,3),((0,-4,3),80,3)]:
 bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(Vector((0,0,0))-o.location).to_track_quat('-Z','Y').to_euler();lights.append(o)
def clear():
 for o in list(sc.objects):
  if o.type not in ['CAMERA','LIGHT']:bpy.data.objects.remove(o,do_unlink=True)
def sphere(name,loc,scale,mat):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=40,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;o.data.materials.append(mat)
 for p in o.data.polygons:p.use_smooth=True
 return o
def render(name,w=640,h=640,ortho=3.5):
 sc.render.resolution_x=w;sc.render.resolution_y=h;cam.data.ortho_scale=ortho;sc.render.filepath=OUT+'/'+name+'.png';bpy.ops.render.render(write_still=True)
def rod(a,b,r=.035,mat=black):
 a,b=Vector(a),Vector(b);bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=r,depth=(b-a).length,location=(a+b)/2);o=bpy.context.object;o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();o.data.materials.append(mat);return o
font=bpy.data.fonts.load('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')
for digit in '0123456789-':
 clear();bpy.ops.object.text_add();o=bpy.context.object;o.data.body=digit;o.data.font=font;o.data.align_x='CENTER';o.data.align_y='CENTER';o.data.size=2.25;o.data.extrude=.13;o.data.bevel_depth=.075;o.data.bevel_resolution=3;o.data.materials.append(black);o.scale=(.79,1.58,1);o.rotation_euler=(.03,-.11,0);render('digit-'+('minus' if digit=='-' else digit),300,600,3.12)
clear();sphere('Sun',(0,0,0),(1.35,1.35,1.35),red);render('sun')
clear();sphere('Moon',(0,0,0),(1.35,1.35,1.35),white);lights[0].location=(-5,1,-1);lights[1].data.energy=0;lights[2].data.energy=0;sc.world.color=(.005,.005,.005);render('moon');lights[0].location=(-3,4,6);lights[1].data.energy=220;lights[2].data.energy=80;sc.world.color=(.45,.45,.45)
clear()
for x,y,z,s in [(-.85,-.15,0,.63),(-.35,.25,0,.85),(.42,.2,.05,.72),(.95,-.15,0,.5),(0,-.3,.3,.67)]:sphere('Cloud',(x,y,z),(s,s*.8,s*.8),white)
render('cloud')
clear();rod((0,-1.3,0),(0,1.18,0),.028);rod((-1.35,-.1,0),(1.1,-.1,0),.045)
# Compass ring lies back into the image, creating a wide ellipse.
bpy.ops.mesh.primitive_torus_add(major_radius=1.3,minor_radius=.025,major_segments=96,minor_segments=12);ring=bpy.context.object;ring.scale.y=.23;ring.location.y=-.1;ring.data.materials.append(black)
verts=[(.8,-.5,.04),(1.38,-.1,.04),(.8,.3,.04),(.92,-.1,.28)];faces=[(0,1,3),(1,2,3),(2,0,3),(0,2,1)];me=bpy.data.meshes.new('Arrow');me.from_pydata(verts,[],faces);ob=bpy.data.objects.new('Wind arrow',me);sc.collection.objects.link(ob);ob.data.materials.append(black)
for x in [-1.1,-.98]:
 bpy.ops.mesh.primitive_cube_add(size=1,location=(x,-.1,0));o=bpy.context.object;o.scale=(.08,.36,.07);o.rotation_euler.z=.2;o.data.materials.append(black)
for angle in [0,2.094,4.188]:
 end=(math.cos(angle)*.48,.82+math.sin(angle)*.25,math.sin(angle)*.25);rod((0,.82,0),end,.025);sphere('Anemometer cup',end,(.2,.2,.12),black)
render('air')
clear();random.seed(2)
N=12;top=[(math.cos(i*2*math.pi/N)*1.4,.05+math.sin(i*2*math.pi/N)*.27,.1) for i in range(N)];bottom=[(x*.82,y-.25-random.random()*.4,z-.15) for x,y,z in top];verts=top+bottom+[(0,-.85,-.1)];faces=[tuple(range(N))]
for i in range(N):j=(i+1)%N;faces.extend([(i,j,N+i),(j,N+j,N+i),(N+i,N+j,N*2)])
me=bpy.data.meshes.new('Floating terrain');me.from_pydata(verts,[],faces);ob=bpy.data.objects.new('Precipitation terrain',me);sc.collection.objects.link(ob);ob.data.materials.append(black)
for i in range(13):
 x=random.uniform(-1.15,1.15);y=random.uniform(.35,1.35);rod((x,y,0),(x-.07,y-.19,0),.014)
render('precip');bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath('sculptures.blend'))
