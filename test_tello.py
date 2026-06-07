from djitellopy import Tello

# Initialize the Tello drone
tello = Tello()
tello.connect()

# Get battery percentage
print(f"Battery: {tello.get_battery()}%")

# Take off and land test
tello.takeoff()
tello.land()
