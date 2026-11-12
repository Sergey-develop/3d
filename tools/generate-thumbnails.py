import bpy,math,os
from mathutils import Vector
base=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dist', 'assets'))
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
bpy.ops.import_scene.gltf(filepath=os.path.join(base,'base_body.glb'))
def morph():
 for ob in bpy.context.scene.objects:
  if ob.type=='MESH' and ob.data.shape_keys:
   for k in ob.data.shape_keys.key_blocks:
    if k.name!='Basis':k.value=0
   if 'gender_female' in ob.data.shape_keys.key_blocks:ob.data.shape_keys.key_blocks['gender_female'].value=.8
morph()
world=bpy.context.scene.world;world.color=(.22,.22,.22)
bpy.ops.object.light_add(type='AREA', location=(0,-2,3));bpy.context.object.data.energy=450;bpy.context.object.data.shape='DISK';bpy.context.object.data.size=3
bpy.ops.object.camera_add(location=(0,-1.2,1.48));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,1.46))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=.48;bpy.context.scene.camera=cam
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=12;s.render.resolution_x=220;s.render.resolution_y=220;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.film_transparent=False
for hair in ['short02','bob02','long01','ponytail01']:
 before=set(bpy.context.scene.objects);bpy.ops.import_scene.gltf(filepath=os.path.join(base,'hair_'+hair+'.glb'));new=set(bpy.context.scene.objects)-before;morph();s.render.filepath=os.path.join(base,'thumb_'+hair+'.png');bpy.ops.render.render(write_still=True)
 for ob in new:bpy.data.objects.remove(ob,do_unlink=True)
