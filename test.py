



from datetime import datetime
import time
print(datetime.now().isoformat())

current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
print(current_time)

# time.strptime(t, "% d % b % Y % H:% M:% S")
# print (current_time)

# now = datetime.now()
#
# current_time = now.strftime("%H:%M:%S")
# print("Current Time =", current_time)



import json
import os


path = "./dataFromCp"
if not os.path.exists(path):
    os.makedirs(path)
else:
    pass


data= {'charge_point_model': 'Optimus', 'charge_point_vendor': 'NOEVmh_vendor'}
data["local time"] = current_time

jsondata = json.dumps(data,indent=4,separators=(',', ': '))
with open('./dataFromCp/filename.json', 'w') as f:
    f.write(jsondata)


def add(A=3, b=9):
    print (A+b)




Json.stringify([2,id,"DataTransfer",{
            vendor_id="MOEV_GUI",
            message_id="start remote transaction",
            data={
                "cp_id": "CP_m",
                "max_watts": 1200,
                "max_current": None,
                }
            }])



{"cp_id":CP_1,"max_watts": 1200, "max_current": -1}