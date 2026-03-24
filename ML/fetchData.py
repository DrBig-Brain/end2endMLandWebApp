import subprocess

months = [f"{i:02d}" for i in range(1, 13)]

base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data"

for month in months:
    url = f"{base_url}/yellow_tripdata_2025-{month}.parquet"
    
    try:
        print(f"Downloading month {month}...")
        
        subprocess.run(
            ["wget", "-P", "./ML/Data", url],
            check=True
        )
        
        print(f"Successfully downloaded {month}\n")
        
    except subprocess.CalledProcessError as e:
        print(f"Failed for month {month}: {e}\n")