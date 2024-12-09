# Airfoil-Mesh-Generation
An unstrustured 2D circular control volume mesh generator for airofil geometries.
Developed for Athens week Nov24 - ENSAM Paristech ENSAM /TUD01 Introduction into Finite Elements and Algorithms Course. Written in Julia.

FLUID FLOW CONTROL VOLUME MESH GENERATION

Mesh generation for a 2D fluid flow control volume problem involves discretizing the problem domain (the control volume) into smaller, non-overlapping elements, typically triangles or quadrilaterals, to create a computational grid. This grid enables numerical methods, such as Computational Fluid Dynamics (CFD), to solve the governing fluid flow equations, such as the Navier-Stokes equations. The mesh is designed to capture the geometry of the control volume accurately, ensuring fine resolution near important features like boundaries, walls, or regions with high gradients (e.g., velocity or pressure). The mesh must be structured or unstructured, depending on the complexity of the geometry, and it must be refined in regions where greater accuracy is needed, such as in areas with strong flow variations or boundary layers, to ensure reliable and efficient simulation results.


1- Importing the Packages

This code imports the Gmsh package, which is a popular tool for mesh generation, enabling the creation and manipulation of geometric models and computational grids for simulations. It also imports the LinearAlgebra module, which provides functions and types for performing various linear algebra operations such as matrix manipulation, solving linear systems, and eigenvalue problems. Additionally, the Plots package is imported to enable data visualization, allowing the user to generate a variety of plots and graphs to represent data. These imports together suggest the code might be used for mesh-based simulations and numerical computations, potentially visualizing results graphically.


2- Defining a Function for Generating the Coordinates of a Circle

This function generates the coordinates of points evenly spaced along the circumference of a circle. The function takes three inputs: center, radius and number of elements. The x and y coordinates of each point are calculated using basic trigonometric functions, and the resulting points are stored in the points list. Finally, the function returns the list of points as tuples of coordinates.

![image](https://github.com/user-attachments/assets/c1e27576-dbd3-4f17-b791-29bfcdaaf415)


3- Defining a Function for Generating the Coordinates of an Airfoil

This function defines naca_4digit that generates the coordinates of a NACA 4-digit airfoil based on the given parameters. The function takes four inputs:
- m (maximum camber)
- p (position of the maximum camber)
- t (thickness)
- n_points (number of points used to represent the airfoil)
The camber line (y_c) is computed in two sections: for x[i] less than p, a parabolic equation is used, and for x[i] greater than p, another parabolic equation applies. The thickness distribution (y_t) is calculated using a standard formula for NACA airfoils. The upper and lower surface coordinates (y_u and y_l) are obtained by adding and subtracting the thickness, respectively, from the camber line. The code then combines the upper and lower surface points by concatenating them in reverse order to create a closed loop of coordinates, which is returned as a list of (x, y) tuples representing the full airfoil shape.

![image](https://github.com/user-attachments/assets/c2134fb0-b535-4e8d-a75a-74e99599fcf7)


4- Defining a Function for Generating the Control Volume Mesh

The main function creates a 2D mesh for a "donut-shaped" geometry using the Gmsh library. The function takes four inputs: outer_vertices and inner_vertices (lists of coordinates for the outer and inner circles, respectively), and lc_outer and lc_inner (local mesh sizes for the outer and inner circles). It initializes Gmsh and sets up a new model. Then, it generates points for both the outer and inner circles, assigning them appropriate mesh resolutions. Next, the function creates boundary lines connecting the points of both circles. Afterward, it defines two curve loops to represent the outer boundary and inner hole, and a plane surface is created to form the donut shape. The geometry is synchronized with Gmsh, and a 2D mesh is generated. The resulting mesh is optionally written to a file and visualized using Gmsh's graphical user interface. Finally, Gmsh is finalized to clean up resources. This function allows for the creation of a custom 2D mesh for a domain with a circular hole.

![image](https://github.com/user-attachments/assets/330a4ef7-f2d1-4349-b07b-951e98030804)


5- Obtaining the Coordinates of Inner and Outer Boundaries

To define the control volume boundaries, a grater circle is generated as the outer boundary with the relevant function. For the inner boundary a generic NACA 2412 airfoil is defined using the presented function with necessray number of surface panels that match the mesh size which will be defined below.


6- Generating the Mesh Inside the Control Volume

Between two boundaries a triangular mesh is generated using the main mesh generation function. The elements size decreases from outer boundary to inner boundary. Which is necessary for a 2D fluid flow solver to calculate important aerodynamic phenomena around the airfoil surface.

![image](https://github.com/user-attachments/assets/72361148-81b2-400f-bdff-3b1a6f26bf54)


7- Refining the Mesh

When generating a 2D airfoil mesh, the key factors to consider are element size and mesh density. Element size refers to the spacing between mesh points, which influences the accuracy of the simulation; smaller elements lead to higher resolution and more accurate results, particularly in regions with steep gradients like the leading edge, trailing edge, and boundary layers. Mesh density, which defines how finely the domain is discretized, should be higher near the airfoil surface where the flow features (such as velocity and pressure variations) are most significant.

In contrast, the mesh can be coarser farther away from the airfoil to reduce computational cost. The distribution of mesh density is also important—using a finer mesh near the airfoil and gradually coarser elements away from the surface is common. Proper mesh refinement ensures accurate results without excessive computational expense, and a well-distributed mesh avoids introducing numerical errors or inefficiencies in simulation.

![image](https://github.com/user-attachments/assets/0affd8e6-e478-404c-a6cf-66ea95927885)













