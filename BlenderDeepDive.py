# Import bpy module
import bpy

# Enable the "Import Images as Planes" add-on
bpy.ops.preferences.addon_enable(module="io_import_images_as_planes")

# Get the file name from user input or use a default value
file_name = input("Enter the file name of the depth map image: ") or "depth_map.png"

# Get the scale value from user input or use a default value
scale_value = float(input("Enter the scale value for the displacement: ")) or 0.1

# Get the dicing rate from user input or use a default value
dicing_rate = float(input("Enter the dicing rate for the adaptive subdivision: ")) or 1

# Try to import the depth map image as a plane
try:
    bpy.ops.import_image.to_plane(files=[{"name":file_name}])
except RuntimeError as e:
    print("Error: ", e)
    exit()

# Get the plane object and its material
plane = bpy.context.selected_objects[0]
mat = plane.material_slots[0].material

# Set the map texture node to non-color data
map_node = mat.node_tree.nodes["Image Texture"]
map_node.image.colorspace_settings.name = "Non-Color"

# Add a subdivision modifier to the plane
subdiv = plane.modifiers.new("Subdivision", "SUBSURF")
subdiv.subdivision_type = "SIMPLE"

# Enable adaptive subdivision and set the dicing rate
bpy.context.scene.cycles.use_adaptive_subdivision = True
plane.cycles.dicing_rate = dicing_rate

# Add a displacement node and connect it to the material output node
disp_node = mat.node_tree.nodes.new("ShaderNodeDisplacement")
output_node = mat.node_tree.nodes["Material Output"]
mat.node_tree.links.new(disp_node.outputs["Displacement"], output_node.inputs["Displacement"])

# Set the displacement node settings
disp_node.inputs["Scale"].default_value = scale_value # Adjust this value as needed
disp_node.inputs["Midlevel"].default_value = 0.5

# Connect the map texture node to the displacement node
mat.node_tree.links.new(map_node.outputs["Color"], disp_node.inputs["Height"])
