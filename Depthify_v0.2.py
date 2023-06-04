# Depthify v0.2: Bing explains: is a continuation of the code revision that adds some docstrings and comments to explain how the code revision works:
#according to bing 0.1 rewrite represents the: next logical revision for the existing script that would implement as much as possible of what we’ve discussed, while keeping the complexity of the changes minimal
#Create realistic and stunning 3D surfaces from depth map images in Blender.
# This script imports and transforms a depth map image into a 3D surface in Blender.
# It uses some modules and features such as bpy, numpy, argparse, etc. to enhance the quality, usability, and functionality of the script.

# Import the modules
import bpy
import numpy as np
import argparse
import sys

# Define a function to parse and validate the command line arguments
def parse_args():
    # Create an argument parser object
    parser = argparse.ArgumentParser(description="Depthify: Create realistic and stunning 3D surfaces from depth map images in Blender.")
    # Add some arguments to the parser
    parser.add_argument("file_name", type=str, help="The file name of the depth map image.")
    parser.add_argument("scale", type=float, default=0.2, help="The scale value for the displacement modifier. Default is 0.2.")
    parser.add_argument("dicing_rate", type=float, default=0.5, help="The dicing rate for the adaptive subdivision modifier. Default is 0.5.")
    # Parse the arguments and return them
    args = parser.parse_args()
    # Validate the arguments and exit with an error message if invalid
    if not args.file_name.endswith(".png"):
        sys.exit("Error: The file name must be a PNG image.")
    if not 0 < args.scale < 1:
        sys.exit("Error: The scale value must be between 0 and 1.")
    if not 0 < args.dicing_rate < 1:
        sys.exit("Error: The dicing rate must be between 0 and 1.")
    return args

# Define a function to import and transform the depth map image into a 3D surface in Blender
def depthify(file_name, scale, dicing_rate):
    # Delete the default cube object
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    # Import the depth map image as a plane object
    bpy.ops.import_image.to_plane(files=[{"name": file_name}])
    # Get the plane object and its data
    plane = bpy.context.active_object
    plane_data = plane.data
    # Set the origin of the plane to its center
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="MEDIAN")
    # Set the shading of the plane to smooth
    bpy.ops.object.shade_smooth()
    # Add a subdivision surface modifier to the plane
    sub_mod = plane.modifiers.new(name="Subdivision", type="SUBSURF")
    # Set the subdivision levels to 2 for viewport and render
    sub_mod.levels = 2
    sub_mod.render_levels = 2
    # Enable adaptive subdivision for render
    sub_mod.use_subsurf_uv = True
    sub_mod.use_adaptive_subdivision = True
    # Set the dicing rate for adaptive subdivision
    sub_mod.dicing_rate = dicing_rate
    # Add a displacement modifier to the plane
    dis_mod = plane.modifiers.new(name="Displacement", type="DISPLACE")
    # Set the texture of the displacement modifier to the depth map image
    dis_tex = bpy.data.textures.new(name="Displacement Texture", type="IMAGE")
    dis_tex.image = bpy.data.images[file_name]
    dis_mod.texture = dis_tex
    # Set the coordinates of the displacement modifier to UV
    dis_mod.texture_coords = "UV"
    # Set the strength of the displacement modifier to the scale value
    dis_mod.strength = scale

# Call the parse_args function and get the arguments
args = parse_args()
# Call the depthify function with the arguments
depthify(args.file_name, args.scale, args.dicing_rate)
