import json
from datetime import datetime

import matplotlib.pyplot as plt


with open('fitbit_data.json') as f:
    data = json.load(f)

steps = data['activities-log-steps']

x = [datetime.strptime(d['dateTime'], '%Y-%M-%d').strftime("%A") for d in steps]
y = [float(d['value']) for d in steps]

plt.bar(x,y)
plt.title('Steps last 7 days')
plt.show()
