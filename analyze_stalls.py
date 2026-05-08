import sys
import re

def analyze_stalls(log_filepath):
    timestamps = []
    
    # Regex to find the uncommented Salsify log line: [1778035630901] Frame 45: ...
    # We capture the number inside the brackets.
    log_pattern = re.compile(r"^\[(\d+)\]\s+Frame\s+\d+\s+sent")

    try:
        with open(log_filepath, "r") as file:
            for line in file:
                match = log_pattern.match(line.strip())
                if match:
                    # Convert timestamp from string to integer (milliseconds)
                    timestamps.append(int(match.group(1)))
    except FileNotFoundError:
        print(f"Error: Could not find log file {log_filepath}")
        return

    if len(timestamps) < 2:
        print("Not enough successful frames to calculate stall duration.")
        return

    # Calculate the gaps (stalls) between consecutive frames
    stalls_ms = []
    for i in range(1, len(timestamps)):
        gap = timestamps[i] - timestamps[i - 1]
        stalls_ms.append(gap)

    max_stall = max(stalls_ms)
    avg_stall = sum(stalls_ms) / len(stalls_ms)
    
    # Convert to seconds for easier reading if the stalls are huge
    print(f"--- Stall Analysis for {log_filepath} ---")
    print(f"Total Frames Sent: {len(timestamps)}")
    print(f"Average Stall:     {avg_stall:.2f} ms")
    print(f"MAXIMUM STALL:     {max_stall} ms ({max_stall/1000:.2f} seconds)")
    print("-" * 40)

if __name__ == "__main__":
    # Use the file passed in the terminal, or default to s3_720p_run.log
    target_log = sys.argv[1] if len(sys.argv) > 1 else "s3_720p_run.log"
    analyze_stalls(target_log)
