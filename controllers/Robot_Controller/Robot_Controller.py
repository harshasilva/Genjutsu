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

def getXYfromgps():
    """
    Retrieves the current GPS values and calculates the maze tile coordinates.
    Prints the current state of the robot.
    Returns: A list [x, y] representing the current tile index (0-11).
    """
    gps_vals = gps.getValues()
    
    tile_length = 0.25
    start_gps_x = 1.380
    start_gps_y = -1.388
    
    # Calculate offset from start GPS position
    rel_x = start_gps_x - gps_vals[0]
    rel_y = gps_vals[1] - start_gps_y
    
    # Map distance to grid index 0-11
    new_x = int(round(rel_x / tile_length))
    new_y = int(round(rel_y / tile_length))
    
    # Clip results to 0-11 for 12x12 maze
    new_x = max(0, min(new_x, 11))
    new_y = max(0, min(new_y, 11))
    
    # Output the current state to the terminal
    print(f"X={new_x},Y={new_y};")
    
    return [new_x, new_y]

# 4. Main Loop
prev_gps_vals = [0, 0, 0]

while robot.step(timestep) != -1:
    
    # Get GPS values [x, y, z]
    gps_vals = gps.getValues()
    
    # Calculate current tile coordinate using the new function
    maze_coord = getXYfromgps()
    
    # Calculate the change in coordinate (new - old)
    
    # ---------------------------------------------------------
    # CONTESTANTS: Add your sensor reading, movement, and logic here.
    # ---------------------------------------------------------
    
    # Example: print(f"Position change: {diff_x:.3f}, {diff_y:.3f}")
    
    # Example: print(f"Current Maze Coordinate: {maze_coord}")
    
    # Example of sending a message when your custom condition is met:
    # if my_wall_detected_condition:
    #     send_message("Red")

    pass