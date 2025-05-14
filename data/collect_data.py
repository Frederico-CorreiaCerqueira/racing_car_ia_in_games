import csv

def save_data(sensor_values, action):
    with open('training_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(sensor_values + [action])
