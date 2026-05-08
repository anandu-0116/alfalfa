import re
import statistics
import os

def analyze_cif_logs():
    files = {
        "CONVENTIONAL": "conventional_cif.log",
        "S2 (STRICT DELAY)": "s2_cif.log",
        "S3 (GAME-AWARE)": "s3_cif.log"
    }

    # Regex patterns for our new log format
    sent_pattern = re.compile(r"^\[(\d+)\]\s+Frame\s+\d+\s+sent")
    skip_pattern = re.compile(r"Skipping frame")

    # Print the comprehensive table header
    print(f"\n{'Protocol Mode':<18} | {'Frames Sent':<12} | {'Success Rate':<13} | {'Effective FPS':<14} | {'Avg Stall (ms)':<15} | {'Max Stall (ms)':<15} | {'Jitter (SD ms)':<15}")
    print("-" * 115)

    for mode_name, filename in files.items():
        if not os.path.exists(filename):
            print(f"{mode_name:<18} | ERROR: {filename} not found. Did you run this mode?")
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
            print(f"{mode_name:<18} | ERROR: Not enough data points.")
            continue

        # Calculate Stalls
        stalls = [timestamps[i] - timestamps[i - 1] for i in range(1, len(timestamps))]
        total_time_s = (timestamps[-1] - timestamps[0]) / 1000.0

        # Calculate Metrics
        frames_sent = len(timestamps)
        fps = frames_sent / total_time_s if total_time_s > 0 else 0
        avg_stall = sum(stalls) / len(stalls)
        max_stall = max(stalls)
        jitter = statistics.stdev(stalls) if len(stalls) > 1 else 0
        
        # QoE Metric: Frame Success Rate
        total_attempted = frames_sent + skipped_count
        success_rate = (frames_sent / total_attempted) * 100 if total_attempted > 0 else 0

        # Print the row
        print(f"{mode_name:<18} | {frames_sent:<12} | {success_rate:>5.1f}%        | {fps:<14.2f} | {avg_stall:<15.2f} | {max_stall:<15.2f} | {jitter:<15.2f}")
    
    print("-" * 115)
    print("NOTE: Lower Max Stall and Jitter indicate a smoother user experience.\n")

if __name__ == "__main__":
    analyze_cif_logs()
