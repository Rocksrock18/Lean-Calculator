# Lean-Calculator
API that takes formatted data about a utility pole and returns a number representing how much the pole is leaning.

## Additional Resources
- Repo for front-end:
- Repo for AirSim autopilot:

## Calling the API
You can make a POST request to: https://lean-calculator.herokuapp.com/api

The data you send to the API must be of the following form:

`
{   
  pole: {coordinates:[ , ]}
  image: {fov: , yaw: , width: , height: , latitude: , longitude: , type: , azimuth: , heading: }
  esri_data: {assets: {pole: , crossarm: , insulator: }}
  bounded_box: [ , , , ]
}
`

The API will return a number representing the **lean factor**.

## How It Works
In order to estimate how much a pole is leaning, we first calculate 3 factors:
* Difference in degrees from center of camera to location of pole.
  * Yaw, azimuth, and heading are used to calculate this. Poles further away from the center tend to appear like they are leaning more than they actually are
* Distance from camera to pole
  * Pythagorean Theorem can be used on the difference between the latitude and logitude coordinates of the camera and pole respectively
* Ratio of the bounded_box's area to the y:x ratio of the bounded_box
  * Scaled with image resolution. A larger ratio implies more lean
  
Each factor is then *scaled* and combined to reach the final output.

### Interpreting Results
- Most normal poles will have a leaning factor < 2.
- Anything above 10 means the pole is heavily leaning.

## Authors
* Jasen Lai
* Jaewook Lee
* Arnold Makarov
* Jacob Maxson
