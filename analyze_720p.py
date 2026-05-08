import re
import statistics
import os

def analyze_720p_logs():
    # Targeted 720p log files
    files = {
        "CONVENTIONAL": "conventional_720p_slow.log",
        "S2 (STRICT DELAY)": "s2_720p_slow.log",
        "S3 (GAME-AWARE)": "s3_720p_slow.log"
    }

    # Regex patterns for Salsify log format
    sent_pattern = re.compile(r"^\[(\d+)\]\s+Frame\s+\d+\s+sent")
    skip_pattern = re.compile(r"Skipping frame")

    print(f"\n{'Protocol Mode':<18} | {'Frames Sent':<12} | {'Success Rate':<13} | {'Effective FPS':<14} | {'Avg Stall (ms)':<15} | {'Max Stall (ms)':<15} | {'Jitter (SD ms)':<15}")
    print("-" * 115)

    for mode_name, filename in files.items():
        if not os.path.exists(filename):
            print(f"{mode_name:<18} | ERROR: {filename} not found.")
            continue

        timestamps = []
        skipped_count = 0

        with open(filename, "r") as f:
            for line in f:
                sent_match = sent_pattern.match(line.strip())
                if sent_match:
                    timestamps.append(int(sent_match.group(1)))
                elif skip_pattern.search(line):
                    skipped_count += 1

        if len(timestamps) < 2:
            print(f"{mode_name:<18} | ERROR: Insufficient frames.")
            continue

        # Calculate Stalls
        stalls = [timestamps[i] - timestamps[i - 1] for i in range(1, len(timestamps))]
        total_time_s = (timestamps[-1] - timestamps[0]) / 1000.0

        # Metrics
        frames_sent = len(timestamps)
        fps = frames_sent / total_time_s if total_time_s > 0 else 0
        avg_stall = sum(stalls) / len(stalls)
        max_stall = max(stalls)
        jitter = statistics.stdev(stalls) if len(stalls) > 1 else 0
        
        # Success Rate calculation
        total_attempted = frames_sent + skipped_count
        success_rate = (frames_sent / total_attempted) * 100 if total_attempted > 0 else 0

        print(f"{mode_name:<18} | {frames_sent:<12} | {success_rate:>5.1f}%        | {fps:<14.2f} | {avg_stall:<15.2f} | {max_stall:<15.2f} | {jitter:<15.2f}")
    
    print("-" * 115)
    print("NOTE: 720p runs show the impact of high-resolution compute and network pressure.\n")

if __name__ == "__main__":
    analyze_720p_logs()
