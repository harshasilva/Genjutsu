from controller import Robot

# 1. Initialize Robot
robot = Robot()
timestep = int(robot.getBasicTimeStep())

# 2. Setup Emitter (Required for sending messages to supervisor)
# Make sure the device name matches the emitter name on your Webots node
emitter = robot.getDevice('emitter_2')

# 3. Setup GPS
gps = robot.getDevice('gps')
gps.enable(timestep)

def send_message(message_string):
    """
    Sends a string message to the supervisor.
    """
    binary_data = message_string.encode('utf-8')
    result = emitter.send(binary_data)

    if result == 1:
        print(f"E-puck: '{message_string}' sent successfully!")
        return True
    else:
        return False

print("E-puck: Controller initialized. Waiting for contestant logic...")

# Global variable to track current position in discrete maze coordinates
current_pos = [0, 0]

def cordinate(dist_x, dist_y):
    """
    Calculates the maze coordinate (tile index) relative to (0,0) at GPS (1.380, -1.388).
    Each tile is 0.25m.
    Green arrow = X axis, Red arrow = Y axis, Blue arrow = Z axis.
    """
    global current_pos
    tile_length = 0.25
    
    # Starting (0,0) tile GPS center
    start_gps_x = 1.380
    start_gps_y = -1.388
    
    # Calculate offset from start GPS position
    # If the tile index doesn't change when moving along X, the axis might be inverted.
    # We use (start - current) instead of (current - start) for rel_x.
    rel_x = start_gps_x - dist_x
    rel_y = dist_y - start_gps_y
    
    # Map distance to grid index 0-11
    # We use max(0, ...) to ensure we don't get negative indices if moving 'backwards'
    new_x = int(round(rel_x / tile_length))
    new_y = int(round(rel_y / tile_length))
    
    # Clip results to 0-11 for 12x12 maze
    new_x = max(0, min(new_x, 11))
    new_y = max(0, min(new_y, 11))
    
    current_pos = [new_x, new_y]
    return current_pos

def get_x_y_from_gps():
    """
    Retrieves the current GPS values and calculates the maze tile coordinates.
    Returns: A list [x, y] representing the current tile index (0-11).
    """
    gps_vals = gps.getValues()
    # maze_coord is a list [x, y]
    maze_coord = cordinate(gps_vals[0], gps_vals[1])
    return maze_coord

# 4. Main Loop
prev_gps_vals = [0, 0, 0]

while robot.step(timestep) != -1:
    
    # Get GPS values [x, y, z]
    gps_vals = gps.getValues()
    
    # Calculate current tile coordinate using GPS (x and y)
    maze_coord = cordinate(gps_vals[0], gps_vals[1])
    
    # Display GPS values and Tile Address in console
    print(f"GPS: ({gps_vals[0]:.3f}, {gps_vals[1]:.3f}) | Tile: {maze_coord}")
    
    # Calculate the change in coordinate (new - old)
    diff_x = gps_vals[0] - prev_gps_vals[0]
    diff_y = gps_vals[1] - prev_gps_vals[1]
    
    # Update previous position for the next step
    prev_gps_vals = list(gps_vals)
    
    # Calculate current tile coordinate using GPS (x and y)
    maze_coord = cordinate(gps_vals[0], gps_vals[1])
    
    # ---------------------------------------------------------
    # CONTESTANTS: Add your sensor reading, movement, and logic here.
    # ---------------------------------------------------------
    
    # Example: print(f"Position change: {diff_x:.3f}, {diff_y:.3f}")
    
    # Example: print(f"Current Maze Coordinate: {maze_coord}")
    
    # Example of sending a message when your custom condition is met:
    # if my_wall_detected_condition:
    #     send_message("Red")

    pass