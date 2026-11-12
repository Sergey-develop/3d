import bpy,sys
bpy.ops.import_scene.fbx(filepath=sys.argv[sys.argv.index('--')+1])
for o in bpy.context.scene.objects:
 if o.type=='ARMATURE':
  print('ARMATURE',o.name,'bones',len(o.data.bones)); print('FACIAL', [b.name for b in o.data.bones if any(x in b.name.lower() for x in ['head','eye','jaw','face','lip','brow'])][:100])
for img in bpy.data.images: print('IMAGE',img.name,'packed',bool(img.packed_file),'path',img.filepath)
