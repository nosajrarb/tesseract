import pygame
import math
from colorsys import hsv_to_rgb

pygame.init()

WIDTH, HEIGHT = 1200, 800
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced Rotating Tesseract")
clock = pygame.time.Clock()


vertices = [
    [-1, -1, -1, -1],
    [1, -1, -1, -1],
    [1, 1, -1, -1],
    [-1, 1, -1, -1],
    [-1, -1, 1, -1],
    [1, -1, 1, -1],
    [1, 1, 1, -1],
    [-1, 1, 1, -1],
    [-1, -1, -1, 1],
    [1, -1, -1, 1],
    [1, 1, -1, 1],
    [-1, 1, -1, 1],
    [-1, -1, 1, 1],
    [1, -1, 1, 1],
    [1, 1, 1, 1],
    [-1, 1, 1, 1]
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # Bottom face
    (4, 5), (5, 6), (6, 7), (7, 4),  # Top face
    (0, 4), (1, 5), (2, 6), (3, 7),  # Connecting edges
    (8, 9), (9, 10), (10, 11), (11, 8),  # Inner bottom face
    (12, 13), (13, 14), (14, 15), (15, 12),  # Inner top face
    (8, 12), (9, 13), (10, 14), (11, 15),  # Inner connecting edges
    (0, 8), (1, 9), (2, 10), (3, 11),  # Outer connecting edges
    (4, 12), (5, 13), (6, 14), (7, 15)   # Outer connecting edges
]

def project_4d_to_3d(point, projection_distance):
    """Project 4D point to 3D space using perspective projection"""
    factor = 1 / (projection_distance - point[3])
    return [point[0] * factor, point[1] * factor, point[2] * factor]

def project_3d_to_2d(point):
    """Project 3D point to 2D screen coordinates"""
    scale = 200  
    x = point[0] * scale + WIDTH // 2
    y = point[1] * scale + HEIGHT // 2
    return (int(x), int(y))

def rotate_4d(point, angle_xy, angle_xz, angle_xw):
    """Rotate a 4D point around different planes"""
    x, y, z, w = point
    
    # XY rotation
    new_x = x * math.cos(angle_xy) - y * math.sin(angle_xy)
    new_y = x * math.sin(angle_xy) + y * math.cos(angle_xy)
    x, y = new_x, new_y
    
    # XZ rotation
    new_x = x * math.cos(angle_xz) - z * math.sin(angle_xz)
    new_z = x * math.sin(angle_xz) + z * math.cos(angle_xz)
    x, z = new_x, new_z
    
    # XW rotation
    new_x = x * math.cos(angle_xw) - w * math.sin(angle_xw)
    new_w = x * math.sin(angle_xw) + w * math.cos(angle_xw)
    x, w = new_x, new_w
    
    return [x, y, z, w]

def get_color(depth):
    """Get color based on depth (w-coordinate)"""
   
    normalized_depth = (depth + 1) / 2
   
    blue = min(255, max(0, int(255 * normalized_depth)))
    return (blue, blue, 255)  


running = True
angle_xy = 0
angle_xz = 0
angle_xw = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
 
    screen.fill(BLACK)
    
    
    angle_xy += 0.005
    angle_xz += 0.007
    angle_xw += 0.009
    
 
    projected_vertices = []
    vertex_colors = []
    
    for vertex in vertices:
  
        rotated = rotate_4d(vertex, angle_xy, angle_xz, angle_xw)
        projected_3d = project_4d_to_3d(rotated, 4)
        projected_2d = project_3d_to_2d(projected_3d)
        projected_vertices.append(projected_2d)
        vertex_colors.append(get_color(rotated[3]))
    

    for edge in edges:
        start = projected_vertices[edge[0]]
        end = projected_vertices[edge[1]]

        color = vertex_colors[edge[0]]
        if not all(0 <= c <= 255 for c in color):
            color = (255, 255, 255)  
        pygame.draw.line(screen, color, start, end, 2)
    

    for i, vertex in enumerate(projected_vertices):
        pygame.draw.circle(screen, vertex_colors[i], vertex, 5)
    

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit() 