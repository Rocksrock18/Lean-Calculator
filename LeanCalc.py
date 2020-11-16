import requests
import math

class LeanCalc():
    def __init__(self):
        self.output_scale = 50
        self.offset_scale = 3000
        self.distance_scale = 8000
    
    # adjusts across 180 line until offset is within fov. Runs at most 2 times.
    def adjustOffset(self, offset, fov):
        while offset < -fov:
            offset = offset+180
        while offset > fov:
            offset = offset-180
        return offset

    # approximates the degrees away from the center of the camera the utility pole is
    def calcOffsetFactor(self, data):
        yaw = data["yaw"] if data["yaw"] > 180 else data["yaw"] + 180 # will treat 270 as straight ahead
        azimuth = data["azimuth"]
        heading = data["heading"]
        fov = data["fov"]
        # from here on, numbers can be ambiguous (360 is the same as 0, etc.); we must adjust the numbers to ensure it is within the view we want
        diff = self.adjustOffset(heading-azimuth, fov)
        correction = yaw-(diff+180+270) if bool(yaw > 270) != bool(heading > azimuth) else yaw-(diff+270) # centers at 270, may adjust across 180 line
        return self.adjustOffset(correction, fov)

    # simple pythagorean theorem to calc distance. Scaled up by distance_scale. Assumed [x, y]
    def calcDistance(self, pole_coordinates, camera_coordinates):
        return math.sqrt(((pole_coordinates[0]-camera_coordinates["longitude"])**2)+((pole_coordinates[1]-camera_coordinates["latitude"])**2))*self.distance_scale

    # returns a number representing the lean factor of a utility pole
    def calcLeanFactor(self, offset, bounding_box, img_height, img_width, distance):
        box_width = float(bounding_box[3]- bounding_box[1])
        box_height = float(bounding_box[2]-bounding_box[0])
        y2x_ratio = ((box_height*box_width)/(img_height*img_width)*(distance)) / ((box_height / box_width)) # scales ratio of height to width by comparing to area.
        return (y2x_ratio - abs(offset)/self.offset_scale)*self.output_scale # factors in pole offset from camera, then scales up value