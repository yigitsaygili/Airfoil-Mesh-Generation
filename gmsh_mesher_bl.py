# Importing the Packages
import numpy as np
import gmsh
from cst_xfoil_v1 import *

# Defining a Function for Generating the Coordinates of a Circle
def generate_boundary(center, radius, num_points):
    points = []
    for i in range(num_points):
        angle = 2 * np.pi * i / num_points
        x = center[0] + radius * np.cos(angle)
        y = center[1] + radius * np.sin(angle)
        points.append((x, y))
    return points

# Defining a Function for Generating the Coordinates of an Airfoil (NACA 4-digit)
def generate_airfoil():
    wu = [0.3, 0.2, 0.1]
    wl = [-0.1, -0.05, -0.01]

    x_coords, y_coords = cst_airfoil(wl, wu)
    x_coords -= 0.5

    combined_coords = list(zip(x_coords, y_coords))
    return combined_coords

# Defining a Function for Generating the Control Volume Mesh
def generate_mesh(outer_vertices, inner_vertices, lc_outer, lc_inner, bl_thickness, bl_layers, bl_growth_rate):
    # Initialize GMSH
    gmsh.initialize()

    # Create a new model and set terminal output
    gmsh.option.setNumber("General.Terminal", 1)
    gmsh.model.add("donut_shape_circles")

    # Generate points for the outer and inner circles
    outer_points = []
    inner_points = []

    # Define outer circle points with local mesh resolution
    for i, (x, y) in enumerate(outer_vertices):
        point_label = gmsh.model.geo.addPoint(x, y, 0, lc_outer, i + 1)
        outer_points.append(point_label)

    # Define inner circle points with local mesh resolution
    for i, (x, y) in enumerate(inner_vertices):
        point_label = gmsh.model.geo.addPoint(x, y, 0, lc_inner, i + len(outer_vertices) + 1)
        inner_points.append(point_label)

    # Define lines (edges) for the outer and inner circles
    outer_lines = []
    inner_lines = []

    # Create the outer boundary lines (connect consecutive points on the outer circle)
    for i in range(len(outer_points)):
        start_point = outer_points[i]
        end_point = outer_points[(i + 1) % len(outer_points)]
        outer_lines.append(gmsh.model.geo.addLine(start_point, end_point, i + 1))

    # Create the inner boundary lines (connect consecutive points on the inner circle)
    for i in range(len(inner_points)):
        start_point = inner_points[i]
        end_point = inner_points[(i + 1) % len(inner_points)]
        inner_lines.append(gmsh.model.geo.addLine(start_point, end_point, i + len(outer_points) + 1))

    # Define two curve loops (one for the outer boundary and one for the inner hole)
    outer_loop = gmsh.model.geo.addCurveLoop(outer_lines, 1)
    inner_loop = gmsh.model.geo.addCurveLoop(inner_lines, 2)

    # Define the surface (donut shape with hole)
    gmsh.model.geo.addPlaneSurface([1, 2], 1)

    # Synchronize geometry with GMSH
    gmsh.model.geo.synchronize()

    # Add boundary layer field to the airfoil
    field_id = gmsh.model.mesh.field.add("BoundaryLayer")
    gmsh.model.mesh.field.setNumbers(field_id, "CurvesList", inner_lines)
    gmsh.model.mesh.field.setNumber(field_id, "hwall_n", bl_thickness)  # Height of the first layer
    gmsh.model.mesh.field.setNumber(field_id, "thickness", bl_thickness * ((bl_growth_rate ** bl_layers - 1) / (bl_growth_rate - 1)))  # Total thickness of boundary layer
    gmsh.model.mesh.field.setNumber(field_id, "ratio", bl_growth_rate)  # Growth rate of layers


    # Set the boundary layer field as active
    gmsh.model.mesh.field.setAsBoundaryLayer(field_id)

    # Generate mesh
    gmsh.model.mesh.generate(2)

    # Write mesh to file (optional)
    gmsh.write("airfoil_mesh_with_boundary_layer.msh")

    # Visualize the mesh using GMSH GUI (optional)
    gmsh.fltk.run()

    # Finalize GMSH
    gmsh.finalize()

# Obtaining the Coordinates of Inner and Outer Boundaries
outer_vertices = generate_boundary((0.0, 0.0), 2.0, 20)
inner_vertices = generate_airfoil()

# Parameters for Boundary Layer
bl_thickness = 0.01  # Thickness of the first boundary layer element
bl_layers = 10       # Number of layers in the boundary layer
bl_growth_rate = 1.2 # Growth rate of the layer thickness

# Generate the mesh with a boundary layer
generate_mesh(outer_vertices, inner_vertices, 0.1, 0.01, bl_thickness, bl_layers, bl_growth_rate)

