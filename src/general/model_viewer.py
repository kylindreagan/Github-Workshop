import pygame
import numpy as np
import sys
import os
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def load_off(filename):
    """Load an OFF file and return vertices and faces"""
    with open(filename, 'r') as f:
        # Read header
        line = f.readline().strip()
        if line != 'OFF' and line != 'COFF' and line != 'NOFF':
            # Some OFF files have counts in the first line
            if line.startswith('OFF'):
                line = line[3:].strip()
            else:
                # Try to read as OFF anyway
                pass
        
        # Read counts (skip comment lines)
        while True:
            line = f.readline().strip()
            if not line.startswith('#') and line != '':
                break
        
        # Parse vertex, face, edge counts
        try:
            n_vertices, n_faces, _ = map(int, line.split())
        except:
            # Try to handle malformed first line
            parts = line.split()
            if len(parts) >= 3:
                n_vertices, n_faces = int(parts[0]), int(parts[1])
            else:
                # Read next line
                line = f.readline().strip()
                n_vertices, n_faces, _ = map(int, line.split())
        
        # Read vertices
        vertices = []
        for _ in range(n_vertices):
            while True:
                line = f.readline().strip()
                if not line.startswith('#') and line != '':
                    break
            vertex = list(map(float, line.split()[:3]))
            vertices.append(vertex)
        
        # Read faces
        faces = []
        for _ in range(n_faces):
            while True:
                line = f.readline().strip()
                if not line.startswith('#') and line != '':
                    break
            
            parts = list(map(int, line.split()))
            if parts[0] == 3:
                # Triangle
                faces.append(parts[1:4])
            elif parts[0] == 4:
                # Quad - split into two triangles
                faces.append([parts[1], parts[2], parts[3]])
                faces.append([parts[1], parts[3], parts[4]])
            else:
                # Polygon with more than 4 vertices - triangulate naively
                for i in range(2, parts[0]):
                    faces.append([parts[1], parts[i], parts[i+1]])
        
        return np.array(vertices, dtype=np.float32), faces

def normalize_model(vertices):
    """Center and scale the model to fit in the view"""
    # Center the model
    center = np.mean(vertices, axis=0)
    vertices = vertices - center
    
    # Scale to fit in a unit sphere
    max_dist = np.max(np.linalg.norm(vertices, axis=1))
    if max_dist > 0:
        vertices = vertices / (max_dist * 1.5)
    
    return vertices

def draw_model(vertices, faces):
    """Draw the 3D model"""
    glBegin(GL_TRIANGLES)
    for face in faces:
        # Use face normal for flat shading
        if len(face) >= 3:
            v1 = vertices[face[0]]
            v2 = vertices[face[1]]
            v3 = vertices[face[2]]
            
            # Calculate normal
            normal = np.cross(v2 - v1, v3 - v1)
            normal = normal / np.linalg.norm(normal)
            
            glNormal3f(*normal)
            glVertex3f(*v1)
            glVertex3f(*v2)
            glVertex3f(*v3)
    glEnd()

def setup_lighting():
    """Set up basic lighting"""
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    # Light position
    glLightfv(GL_LIGHT0, GL_POSITION, [5, 5, 5, 1])
    
    # Light colors
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.8, 0.8, 0.8, 1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])
    
    # Material properties
    glMaterialfv(GL_FRONT, GL_SPECULAR, [1, 1, 1, 1])
    glMaterialf(GL_FRONT, GL_SHININESS, 50)

def main():
    # Initialize Pygame
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Model Viewer with Music")
    
    # Set up OpenGL
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.15, 1.0)
    
    # Set up perspective
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -3)
    
    # Setup lighting
    setup_lighting()
    
    # Ask for OFF file
    off_file = None
    if len(sys.argv) > 1:
        off_file = sys.argv[1]
    else:
        # Try to find an OFF file in the current directory
        for file in os.listdir('.'):
            if file.lower().endswith('.off'):
                off_file = file
                break
        
        if not off_file:
            print("No OFF file specified. Usage: python script.py <model.off>")
            print("Please provide an OFF file path:")
            off_file = input("> ").strip()
    
    # Load the OFF file
    if not os.path.exists(off_file):
        print(f"File '{off_file}' not found.")
        # Create a simple cube as fallback
        print("Creating a simple cube as fallback...")
        vertices = np.array([
            [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5],
            [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5]
        ], dtype=np.float32)
        faces = [
            [0, 1, 2], [0, 2, 3],  # Front
            [4, 5, 6], [4, 6, 7],  # Back
            [0, 1, 5], [0, 5, 4],  # Bottom
            [2, 3, 7], [2, 7, 6],  # Top
            [0, 3, 7], [0, 7, 4],  # Left
            [1, 2, 6], [1, 6, 5]   # Right
        ]
        print(f"Loaded fallback cube model.")
    else:
        try:
            vertices, faces = load_off(off_file)
            print(f"Loaded {off_file}: {len(vertices)} vertices, {len(faces)} faces")
        except Exception as e:
            print(f"Error loading OFF file: {e}")
            print("Creating a simple cube as fallback...")
            vertices = np.array([
                [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5],
                [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5], [-0.5, 0.5, 0.5]
            ], dtype=np.float32)
            faces = [
                [0, 1, 2], [0, 2, 3],  # Front
                [4, 5, 6], [4, 6, 7],  # Back
                [0, 1, 5], [0, 5, 4],  # Bottom
                [2, 3, 7], [2, 7, 6],  # Top
                [0, 3, 7], [0, 7, 4],  # Left
                [1, 2, 6], [1, 6, 5]   # Right
            ]
    
    # Normalize the model
    vertices = normalize_model(vertices)
    
    # Initialize music
    pygame.mixer.init()
    
    # Try to load a music file
    music_file = None
    music_extensions = ['.mp3', '.wav', '.ogg', '.mid']
    
    # Check for music file in arguments
    if len(sys.argv) > 2:
        music_file = sys.argv[2]
    else:
        # Look for music files in current directory
        for file in os.listdir('.'):
            if any(file.lower().endswith(ext) for ext in music_extensions):
                music_file = file
                break
    
    # Load and play music if available
    if music_file and os.path.exists(music_file):
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            print(f"Playing music: {music_file}")
            print("Music controls: P = Pause/Resume, S = Stop, + = Volume Up, - = Volume Down")
        except Exception as e:
            print(f"Could not play music file: {e}")
            music_file = None
    else:
        print("No music file found. Supported formats: MP3, WAV, OGG, MID")
        print("You can add a music file to the current directory or specify it as the second argument.")
    
    # Rotation variables
    rotation_speed = 0.5  # degrees per frame
    rotation_x = 0
    rotation_y = 0
    auto_rotate = True
    
    # Main loop
    clock = pygame.time.Clock()
    
    # Instructions
    print("\nControls:")
    print("  Mouse drag: Rotate model manually")
    print("  R: Toggle auto-rotation")
    print("  +/-: Change rotation speed")
    print("  ESC or Q: Quit")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    auto_rotate = not auto_rotate
                    print(f"Auto-rotation: {'ON' if auto_rotate else 'OFF'}")
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    rotation_speed += 0.1
                    print(f"Rotation speed: {rotation_speed:.1f}")
                elif event.key == pygame.K_MINUS:
                    rotation_speed = max(0.1, rotation_speed - 0.1)
                    print(f"Rotation speed: {rotation_speed:.1f}")
                elif event.key == pygame.K_p:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                        print("Music paused")
                    else:
                        pygame.mixer.music.unpause()
                        print("Music resumed")
                elif event.key == pygame.K_s:
                    pygame.mixer.music.stop()
                    print("Music stopped")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Mouse wheel up
                    rotation_speed += 0.1
                    print(f"Rotation speed: {rotation_speed:.1f}")
                elif event.button == 5:  # Mouse wheel down
                    rotation_speed = max(0.1, rotation_speed - 0.1)
                    print(f"Rotation speed: {rotation_speed:.1f}")
        
        # Mouse drag rotation
        if pygame.mouse.get_pressed()[0]:
            mouse_dx, mouse_dy = pygame.mouse.get_rel()
            if mouse_dx != 0 or mouse_dy != 0:
                rotation_y += mouse_dx * 0.5
                rotation_x += mouse_dy * 0.5
                auto_rotate = False
        else:
            pygame.mouse.get_rel()  # Reset relative mouse movement
        
        # Auto rotation
        if auto_rotate:
            rotation_y += rotation_speed
        
        # Clear screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Apply rotation
        glPushMatrix()
        glRotatef(rotation_x, 1, 0, 0)
        glRotatef(rotation_y, 0, 1, 0)
        
        # Draw the model with color
        glColor3f(0.4, 0.6, 1.0)  # Blue color
        draw_model(vertices, faces)
        
        glPopMatrix()
        
        # Update display
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

if __name__ == "__main__":
    main()