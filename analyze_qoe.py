import re
import csv
import statistics

def parse_log(filename, mode_name):
    raw_data = []
    
    # Regex for lines with data
    pattern = re.compile(
        r"avg-delay=(?P<delay>\d+)us.*new-quantizer=(?P<q>\d+).*"
        r"emwa-rate=(?P<emwa>\d+)KB.*new-rate=(?P<nr>\d+)KB.*"
        r"change-percentage=(?P<pct>-?\d+\.\d+)"
    )

    with open(filename, 'r') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                raw_data.append({
                    'mode': mode_name,
                    'status': 'SENT',
                    'delay_us': int(match.group('delay')),
                    'quantizer': int(match.group('q')),
                    'new_rate': int(match.group('nr')),
                    'skipped': 0
                })
            elif "Skipping frame" in line:
                raw_data.append({
                    'mode': mode_name,
                    'status': 'SKIPPED',
                    'delay_us': None,
                    'quantizer': None,
                    'new_rate': None,
                    'skipped': 1
                })
    return raw_data

def calculate_metrics(data_list, mode_name):
    # Filter for frames that were actually sent
    sent_frames = [d for d in data_list if d['status'] == 'SENT']
    total_frames = len(data_list)
    sent_count = len(sent_frames)

    if sent_count == 0:
        return {
            'Mode': mode_name,
            'Avg_SSIM_Proxy': 0,
            'Delay_Jitter_us': 0,
            'Avg_Utilization_KB': 0,
            'Frame_Success_Rate': 0.0
        }

    # Extract columns for math
    delays = [d['delay_us'] for d in sent_frames]
    quantizers = [d['quantizer'] for d in sent_frames]
    rates = [d['new_rate'] for d in sent_frames]

    return {
        'Mode': mode_name,
        'Avg_SSIM_Proxy': round(127 - statistics.mean(quantizers), 2),
        'Delay_Jitter_us': round(statistics.stdev(delays), 2) if len(delays) > 1 else 0,
        'Avg_Utilization_KB': round(statistics.mean(rates), 2),
        'Frame_Success_Rate': round(sent_count / total_frames, 4)
    }

# 1. Parse both logs
conv_raw = parse_log('conventional_run.log', 'Conventional')
s2_raw = parse_log('s2_run.log', 'S2')

# 2. Calculate Summaries
conv_summary = calculate_metrics(conv_raw, 'Conventional')
s2_summary = calculate_metrics(s2_raw, 'S2')

# 3. Save Raw Data CSV
with open('comprehensive_qoe_results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['mode', 'status', 'delay_us', 'quantizer', 'new_rate', 'skipped'])
    writer.writeheader()
    writer.writerows(conv_raw + s2_raw)

# 4. Save Summary CSV (The Professor's Table)
with open('qoe_summary_report.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=conv_summary.keys())
    writer.writeheader()
    writer.writerow(conv_summary)
    writer.writerow(s2_summary)

print("Success! Generated 'comprehensive_qoe_results.csv' (raw) and 'qoe_summary_report.csv' (summary).")
