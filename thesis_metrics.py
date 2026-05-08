import sys
import re
import statistics

def run_thesis_analysis():    files = ["conventional_720p_slow.log", "s2_720p_slow.log", "s3_720p_slow.log"]
    
    # Regex to grab the timestamp from our custom C++ logger
    log_pattern = re.compile(r"^\[(\d+)\]\s+Frame\s+\d+\s+sent")

    # Print the table header
    print(f"\n{'Protocol Mode':<18} | {'Frames Sent':<12} | {'Effective FPS':<14} | {'Avg Stall (ms)':<15} | {'Max Stall (ms)':<15} | {'Jitter (SD ms)':<15}")
    print("-" * 100)

    for file in files:
        timestamps = []
        try:
            with open(file, "r") as f:
                for line in f:
                    match = log_pattern.match(line.strip())
                    if match:
                        timestamps.append(int(match.group(1)))
        except FileNotFoundError:
            print(f"{file:<18} | ERROR: File not found. Did you run this mode?")
            continue

        if len(timestamps) < 2:
            print(f"{file:<18} | ERROR: Not enough data points.")
            continue

        # Calculate the gaps between frames
        stalls = [timestamps[i] - timestamps[i - 1] for i in range(1, len(timestamps))]
        
        # Calculate Total Time (Difference between first and last frame in seconds)
        total_time_s = (timestamps[-1] - timestamps[0]) / 1000.0

        # Calculate Metrics
        frames = len(timestamps)
        fps = frames / total_time_s if total_time_s > 0 else 0
        avg_stall = sum(stalls) / len(stalls)
        max_stall = max(stalls)
        jitter = statistics.stdev(stalls) if len(stalls) > 1 else 0

        # Format the mode name nicely
        mode_name = file.replace("_cif.log", "").upper()
        if mode_name == "CONVENTIONAL": mode_name = "CONVENTIONAL"
        if mode_name == "S2": mode_name = "S2 (STRICT DELAY)"
        if mode_name == "S3": mode_name = "S3 (GAME-AWARE)"

        # Print the row
        print(f"{mode_name:<18} | {frames:<12} | {fps:<14.2f} | {avg_stall:<15.2f} | {max_stall:<15.2f} | {jitter:<15.2f}")
    
    print("-" * 100)
    print("NOTE: Lower Max Stall and Jitter indicate a smoother user experience.\n")

if __name__ == "__main__":
    run_thesis_analysis()
