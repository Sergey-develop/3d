import bpy, math, sys
from mathutils import Vector
args=sys.argv[sys.argv.index('--')+1:]
source,dest=args
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=source)
obj=bpy.data.objects['Cloth_dress']; arm=next(o for o in bpy.data.objects if o.type=='ARMATURE')
for ob in list(bpy.context.scene.objects):
 if ob not in (obj,arm):bpy.data.objects.remove(ob,do_unlink=True)
# Shape the original and every morph consistently in the dress's model space.
def shape(co):
 p=co.copy(); z=p.z
 if .52<z<1.32:
  skirt=max(0,min(1,(1.03-z)/.13)); skirt=skirt*skirt*(3-2*skirt)
  waist=max(0,1-abs(z-1.03)/.13)
  waist=waist*waist*(3-2*waist)
  # Small clearance in the torso and a softly shaped skirt, without inflating sleeves.
  p.x*=1+.045*skirt+.025*waist
  p.y=(p.y+.015)*(1+.055*skirt+.035*waist)-.015
  # Ease the bodice around the chest; taper toward sleeves and neck.
  chest=max(0,1-abs(z-1.225)/.095)*max(0,min(1,(.18-abs(p.x))/.055))
  chest=chest*chest*(3-2*chest)
  p.x*=1+.02*chest
  p.y=(p.y+.015)*(1+.065*chest)-.015
  if z<.96:
   fade=min(1,max(0,(.96-z)/.14));a=math.atan2(p.y+.015,p.x)
   fold=(.003*math.cos(10*a+.4)+.0015*math.cos(20*a))*fade
   r=max(.001,math.hypot(p.x,p.y+.015));p.x+=fold*p.x/r;p.y+=fold*(p.y+.015)/r
 return p
if obj.data.shape_keys:
 for key in obj.data.shape_keys.key_blocks:
  for point in key.data:point.co=shape(point.co)
  if key.name!='Basis':key.value=0
else:
 for v in obj.data.vertices:v.co=shape(v.co)
# Low skirt follows pelvis; retain original blend at the waist and all upper garment weights.
pelvis=obj.vertex_groups.get('pelvis') or obj.vertex_groups.new(name='pelvis')
leg_groups=[g for g in obj.vertex_groups if g.name.startswith(('thigh_','calf_','foot_'))]
for v in obj.data.vertices:
 z=v.co.z
 blend=max(0,min(1,(.995-z)/.09));blend=blend*blend*(3-2*blend)
 if not blend:continue
 leg=[];total=0
 for g in leg_groups:
  try:w=g.weight(v.index)
  except RuntimeError:continue
  leg.append((g,w));total+=w
 if total:
  try:old=pelvis.weight(v.index)
  except RuntimeError:old=0
  pelvis.add([v.index],old+total*blend,'REPLACE')
  for g,w in leg:
   new=w*(1-blend)
   if new<.00001:g.remove([v.index])
   else:g.add([v.index],new,'REPLACE')
for poly in obj.data.polygons:poly.use_smooth=True
bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);arm.select_set(True);bpy.context.view_layer.objects.active=arm
bpy.ops.export_scene.gltf(filepath=dest,export_format='GLB',use_selection=True,export_animations=False,export_morph=True,export_skins=True)
