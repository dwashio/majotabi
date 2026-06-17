"""Blender headless script: generate a low-poly tree and export as GLB.
Run: blender --background --python tools/gen_test_tree.py
"""
import bpy
import math

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

mat_trunk = bpy.data.materials.new("Trunk")
mat_trunk.use_nodes = True
mat_trunk.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.45, 0.28, 0.15, 1)

mat_leaves = bpy.data.materials.new("Leaves")
mat_leaves.use_nodes = True
mat_leaves.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.3, 0.65, 0.25, 1)

bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.6, location=(0, 0, 0.3))
trunk = bpy.context.active_object
trunk.name = "Trunk"
trunk.data.materials.append(mat_trunk)

layers = [
    {"z": 0.7, "r": 0.4, "h": 0.35},
    {"z": 1.0, "r": 0.3, "h": 0.3},
    {"z": 1.25, "r": 0.18, "h": 0.25},
]
for i, layer in enumerate(layers):
    bpy.ops.mesh.primitive_cone_add(
        vertices=6,
        radius1=layer["r"],
        radius2=0.02,
        depth=layer["h"],
        location=(0, 0, layer["z"])
    )
    cone = bpy.context.active_object
    cone.name = f"Leaves_{i}"
    cone.data.materials.append(mat_leaves)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.join()
bpy.context.active_object.name = "LowPolyTree"

bpy.ops.export_scene.gltf(
    filepath="assets/models/nature/tree_01.glb",
    export_format='GLB',
    use_selection=True,
    export_apply=True,
)
print("Exported: assets/models/nature/tree_01.glb")
