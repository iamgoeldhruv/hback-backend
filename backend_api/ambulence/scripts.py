import requests
import json
import time

def UpdateLocation(temp):
    waypoints = {
        "coordinates": temp,
        "type": "LineString"
    }
    total_time = 36*180
    x = len(waypoints["coordinates"])
    for i, coordinate in enumerate(waypoints["coordinates"]):
        
        print(i,coordinate[1])
        url = "http://10.61.24.165:8000/api/update-ambulance-location/"
        data = {
        "number_plate": "rustic",
        "current_location_latitude": coordinate[1],  
        "current_location_longitude": coordinate[0], 
        
        }
        time.sleep(1)
        try:
            response = requests.put(url, json=data)

        
            if response.status_code == 200:
                print("Ambulance location updated successfully.")
            else:
                print("\n")
                print("\n")
                print("\n")

                print(response.content)

                print("\n")
                print("\n")
                print("\n")

                print("Failed to update ambulance location.")
                
        except:
            break


        

    



                      


          
 

               

               

     
        
        

     