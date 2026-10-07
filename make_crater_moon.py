import bpy,math,random,os
import numpy as np
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.mesh.primitive_uv_sphere_add(segments=192,ring_count=128,radius=1.35)
o=bpy.context.object;o.name='Moon — cratered hemispheres';mesh=o.data
coords=np.empty(len(mesh.vertices)*3,dtype=np.float32);mesh.vertices.foreach_get('co',coords);coords=coords.reshape((-1,3));normals=coords/np.linalg.norm(coords,axis=1)[:,None];radial=np.full(len(coords),1.35,dtype=np.float32)
random.seed(42)
for i in range(62):
 z=random.uniform(-1,1);az=random.uniform(0,math.tau);c=np.array([math.sqrt(1-z*z)*math.cos(az),math.sqrt(1-z*z)*math.sin(az),z]);size=random.uniform(.06,.17)
 distance=np.sqrt(np.maximum(0,2-2*np.clip(normals@c,-1,1)));q=distance/size
 bowl=-size*.35*np.maximum(0,1-q*q)**2
 rim=size*.085*np.exp(-((q-1)/.14)**2)
 radial+=bowl+rim
# Fine uneven terrain stays part of the mesh and turns with the moon.
radial+=.0025*np.sin(normals[:,0]*88)*np.sin(normals[:,1]*79)*np.sin(normals[:,2]*93)
mesh.vertices.foreach_set('co',(normals*radial[:,None]).ravel());mesh.update()
for name,color in [('Unlit hemisphere',(.002,.002,.003,1)),('Illuminated hemisphere',(.83,.83,.81,1))]:
 m=bpy.data.materials.new(name);m.diffuse_color=color;m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;p.inputs['Roughness'].default_value=1;p.inputs['Metallic'].default_value=0;o.data.materials.append(m)
for p in mesh.polygons:
 p.material_index=0 if sum(mesh.vertices[i].co.x for i in p.vertices)<0 else 1;p.use_smooth=True
bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath('crater_moon.blend'))
bpy.ops.export_scene.gltf(filepath=os.path.abspath('dist/assets/sculptures/moon.glb'),export_format='GLB',use_selection=True)
