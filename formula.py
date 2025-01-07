import bpy
import math
import random

# Clear all existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Parameters
loop_radius = 5  # Radius of the infinity loop
num_points_binary = 50  # Number of points for the binary line
num_points_super = 300  # Number of points for the superpositional line
super_max_offset = 0.05  # Maximum offset for the superpositional line from the binary line
wavelength_min = 0.5  # Minimum wavelength
wavelength_max = 1.0  # Maximum wavelength
scaling_factor = 1.0  # Scaling factor for each stage
height_offset = 0.0  # Height offset for each layer
num_stages = 1  # Number of evolution stages

# Function to create the binary line in the shape of an infinity symbol
def create_binary_line_infinity(loop_radius, num_points, center_offset):
    points = []
    for i in range(num_points):
        t = 2 * math.pi * (i / (num_points - 1))  # Parametric angle along the path
        x = center_offset[0] + loop_radius * math.sin(t)
        y = center_offset[1] + loop_radius * math.sin(t) * math.cos(t)
        z = center_offset[2] + loop_radius * math.cos(t)
        points.append((x, y, z))

    # Create the binary line curve
    curve_data = bpy.data.curves.new('BinaryLineInfinity', type='CURVE')
    curve_data.dimensions = '3D'

    polyline = curve_data.splines.new('POLY')
    polyline.points.add(len(points) - 1)

    for i, coord in enumerate(points):
        x, y, z = coord
        polyline.points[i].co = (x, y, z, 1)

    curve_obj = bpy.data.objects.new('BinaryLineInfinity', curve_data)
    bpy.context.collection.objects.link(curve_obj)

    return points  # Return points for potential connections

# Function to create the superpositional line around the infinity symbol
def create_superposition_line_infinity(binary_points, max_offset, wavelength_min, wavelength_max):
    points = []
    for i, (x, y, z) in enumerate(binary_points):
        offset = random.uniform(-max_offset, max_offset)
        wavelength = random.uniform(wavelength_min, wavelength_max)
        new_x = x + offset * math.sin(i * wavelength)
        new_y = y + offset * math.cos(i * wavelength)
        new_z = z + offset * math.sin(i * wavelength / 2)
        points.append((new_x, new_y, new_z))

    # Create the superpositional line curve
    curve_data = bpy.data.curves.new('SuperpositionLineInfinity', type='CURVE')
    curve_data.dimensions = '3D'

    polyline = curve_data.splines.new('POLY')
    polyline.points.add(len(points) - 1)

    for i, coord in enumerate(points):
        x, y, z = coord
        polyline.points[i].co = (x, y, z, 1)

    curve_obj = bpy.data.objects.new('SuperpositionLineInfinity', curve_data)
    bpy.context.collection.objects.link(curve_obj)

# Function to scale and elevate a new layer
def create_scaled_layer(binary_points, scaling_factor, height_offset):
    scaled_points = []
    for x, y, z in binary_points:
        scaled_points.append((x * scaling_factor, y * scaling_factor, z + height_offset))

    # Create the scaled binary line curve
    curve_data = bpy.data.curves.new('ScaledBinaryLine', type='CURVE')
    curve_data.dimensions = '3D'

    polyline = curve_data.splines.new('POLY')
    polyline.points.add(len(scaled_points) - 1)

    for i, coord in enumerate(scaled_points):
        x, y, z = coord
        polyline.points[i].co = (x, y, z, 1)

    curve_obj = bpy.data.objects.new('ScaledBinaryLine', curve_data)
    bpy.context.collection.objects.link(curve_obj)

    return scaled_points

# Generate the first layer of lines
center_offset = (0, 0, 0)
binary_points = create_binary_line_infinity(loop_radius, num_points_binary, center_offset)
create_superposition_line_infinity(binary_points, super_max_offset, wavelength_min, wavelength_max)

# Generate subsequent evolution stages
for stage in range(1, num_stages + 1):
    loop_radius *= scaling_factor
    binary_points = create_scaled_layer(binary_points, scaling_factor, height_offset * stage)
    create_superposition_line_infinity(binary_points, super_max_offset, wavelength_min, wavelength_max)
