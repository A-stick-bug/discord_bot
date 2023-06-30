import matplotlib.pyplot as plt
import requests


def update_sun_data():
    url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index-forecast.json"
    response = requests.get(url)
    data = response.json()
    
    # Extract time, y and color values from the data
    time_values = [row[0] for row in data[1:]]
    y_values = [float(row[1]) for row in data[1:]]
    color_values = [row[2] for row in data[1:]]
    
    # Create a color map to map color values to colors
    unique_color_values = list(set(color_values))
    cmap = plt.cm.get_cmap('viridis', len(unique_color_values))
    
    # Plot the data
    plt.bar(time_values, y_values, color=[cmap(unique_color_values.index(c)) for c in color_values])
    
    # Set the x-axis ticks to only display the date if the time is 00:00:00
    x_ticks = [t.split()[0] if t.endswith("00:00:00") else "" for t in time_values]
    plt.xticks(range(len(time_values)), x_ticks,fontsize=8)
    
    # Rotate the x-axis labels by 30 degrees
    plt.xticks(rotation=30)
    
    # Add a legend to show the mapping of color values to colors
    plt.legend(handles=[plt.Line2D([0], [0], color=cmap(i), label=unique_color_values[i]) for i in range(len(unique_color_values))])
    
    # Add title and axis labels
    plt.title("Geomagnetic Activity")
    plt.xlabel("Date")
    plt.ylabel("Planetary k-index")
    
    # Save the graph to an image file
    plt.savefig('sun_data.png')
    plt.close()
    