# Lean-Calculator

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
