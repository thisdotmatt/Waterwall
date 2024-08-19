import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.dates as mdates

#Load csv
df = pd.read_csv('flows_data.csv')

df['start_time'] = pd.to_datetime(df['start_time'], unit='s')
df['end_time'] = pd.to_datetime(df['end_time'], unit='s')
print(df['label'])

N = 10 # how far back in time in minutes
chunk_size = 10 # network flow chunk size, in minutes
cutoff_time = df['end_time'].max() - pd.Timedelta(minutes=N)
cutoff_end_time = df['end_time'].max() - pd.Timedelta(minutes=N-chunk_size)
df = df[df['start_time'] >= cutoff_time]
df = df[df['start_time'] <= cutoff_end_time]

#Extract necessary columns
df['duration'] = df['end_time'] - df['start_time']
df['total_packets'] = df['spkts'] + df['dpkts']
df['total_bytes'] = df['sbytes'] + df['dbytes']

fig, ax = plt.subplots(figsize=(12, 6))

for index, row in df.iterrows():
    edge_color = 'blue' if "0" in row['label'] else 'red'
    face_color = 'skyblue' if "0" in row['label'] else 'red'
    rect = patches.Rectangle(
        (row['start_time'], 0),   
        row['duration'],         
        row['total_bytes'],
        linewidth=1,
        edgecolor=edge_color,
        facecolor=face_color,
        alpha=0.6
    )
    ax.add_patch(rect)
    
print(df['start_time'].min(), df['end_time'].max())

plt.xlabel('Time')
plt.ylabel('Total Bytes')
plt.title('Network Flow')

ax.xaxis_date() 
ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

ax.set_xlim(df['start_time'].min(), df['end_time'].max())
ax.set_ylim(0, df['total_bytes'].max() * 1.1)
plt.grid(True)
plt.show()
