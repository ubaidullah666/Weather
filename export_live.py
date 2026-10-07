from pathlib import Path
# Reuse the sculpted temperature geometry, exporting meshes instead of still frames.
s=Path('render_temperature.py').read_text()
s=s.replace("s.render.filepath=os.path.abspath('dist/assets/sculptures/digit-'+('minus' if digit=='-' else digit)+'.png');bpy.ops.render.render(write_still=True)","bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.export_scene.gltf(filepath=os.path.abspath('dist/assets/sculptures/digit-'+('minus' if digit=='-' else digit)+'.glb'),export_format='GLB',use_selection=True)")
s=s.replace("bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath('temperature.blend'))","")
exec(compile(s,'render_temperature.py','exec'))
# Export the weather sculptures with their separate moving parts intact.
s=Path('render_sculptures.py').read_text();a=s.index("for digit in '0123456789-':");b=s.index("clear();sphere('Sun'",a);s=s[:a]+s[b:]
s=s.replace("sc.render.resolution_x=w;sc.render.resolution_y=h;cam.data.ortho_scale=ortho;sc.render.filepath=OUT+'/'+name+'.png';bpy.ops.render.render(write_still=True)","bpy.ops.object.select_all(action='DESELECT')\n for obj in sc.objects:\n  if obj.type=='MESH':obj.select_set(True)\n bpy.ops.export_scene.gltf(filepath=OUT+'/'+name+'.glb',export_format='GLB',use_selection=True)")
s=s.replace("bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath('sculptures.blend'))","")
exec(compile(s,'render_sculptures.py','exec'))
