from opentrons import robot


def connect_to_robot():
    """
    Search for ports, connect to a robot, and home
    """
    ports = robot.get_serial_ports_list()
    if not ports:
        print('\n\nERROR:\n\n')
        print(
            '\n\n\n\nNo serial ports found.\n\nPlease make sure your robot\'s USB cable is connected\n\n')
        while True:
            pass
    
    print('Enter the number of the port to connect to:\n')
    for i, portname in enumerate(ports):
        print('  {0})   {1}\n'.format(i, portname))
    val = input('Enter number next to desired port (0, 1, etc): ')
    try:
        robot.connect(ports[int(val)])
    except RuntimeWarning:
        robot.connect(ports[int(val)])
    
    print('Connected, homing...')
    robot.home('xyz')


def request_distance_from_user():
    """
    Get the dimensions of this robot, and ask the user for the testing distance
    """
    dimensions = robot._driver.get_dimensions() - (50, 50, 0)
    x_dist = int(input('Enter distanct for X to travel (max {}):'.format(dimensions[0])))
    y_dist = int(input('Enter distanct for Y to travel (max {}):'.format(dimensions[1])))
    x_dist = min(x_dist, dimensions[0])
    y_dist = min(y_dist, dimensions[1])
    return (x_dist, y_dist)

    
def measure_belts(x_dist, y_dist):
    """
    Move the robot, allow user to mark positions, ask user to measure and submit measurements
    """
    print('Moving the robot {0}mm on the X, and {1}mm on the Y'.format(x_dist, y_dist))
    robot.move_head(x=x_dist, y=y_dist * -1, mode='relative')  # Y axis is flipped

    input('mark X position on the robot, then press ENTER key')
    input('mark Y position on the robot, then press ENTER key')

    robot.home('xy')
    robot.home('xy')

    actual_travel_x = float(input('enter the measured X distance: '))
    actual_travel_y = float(input('enter the measured Y distance: '))
    robot._driver.calibrate_steps_per_mm('x', x_dist, actual_travel_x)
    robot._driver.calibrate_steps_per_mm('y', y_dist, actual_travel_y)


print('\n\n\n\n********\n\nStarting Belt Calibration\n\n********\n')

connect_to_robot()
x, y = request_distance_from_user()
measure_belts(x, y)

print('New values saved. Restarting the robot to allow changes to take effect')
print('Please wait 5-10 seconds before reconnecting to the robot')

robot._driver.reset()
robot.disconnect()
