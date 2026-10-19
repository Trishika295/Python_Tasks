
import re
from collections import Counter
from pathlib import Path
from datetime import datetime

# Common HTTP access log format:
# IP - - [timestamp] "METHOD /endpoint HTTP/1.1" STATUS SIZE

LOG_PATTERN = re.compile(
    r'(?P<ip>\S+)\s+\S+\s+\S+\s+'
    r'\[(?P<timestamp>[^\]]+)\]\s+'
    r'"(?P<method>[A-Z]+)\s+'
    r'(?P<endpoint>\S+)\s+HTTP/[^"]+"\s+'
    r'(?P<status>\d{3})\s+'
    r'(?P<size>\S+)'
)


def parse_log_line(line):
    """Parse one log line. Return None for malformed entries."""
    match = LOG_PATTERN.search(line.strip())

    if not match:
        return None

    record = match.groupdict()

    try:
        record["status"] = int(record["status"])
        record["size"] = (
            int(record["size"])
            if record["size"].isdigit()
            else 0
        )
    except (ValueError, TypeError):
        return None

    return record


def read_log_file(file_path):
    """Read logs safely and separate valid and malformed lines."""
    records = []
    malformed_lines = 0

    with open(file_path, "r", encoding="utf-8", errors="replace") as file:
        for line in file:
            if not line.strip():
                continue

            record = parse_log_line(line)

            if record is None:
                malformed_lines += 1
            else:
                records.append(record)

    return records, malformed_lines


def analyze_logs(records):
    """Calculate useful statistics from parsed log records."""
    status_counts = Counter()
    ip_counts = Counter()
    endpoint_counts = Counter()
    method_counts = Counter()

    for record in records:
        status = record["status"]

        status_counts[status] += 1
        ip_counts[record["ip"]] += 1
        endpoint_counts[record["endpoint"]] += 1
        method_counts[record["method"]] += 1

    total_requests = len(records)
    error_count = sum(
        count for status, count in status_counts.items()
        if status >= 400
    )

    server_error_count = sum(
        count for status, count in status_counts.items()
        if status >= 500
    )

    client_error_count = sum(
        count for status, count in status_counts.items()
        if 400 <= status < 500
    )

    success_count = sum(
        count for status, count in status_counts.items()
        if 200 <= status < 300
    )

    error_rate = (
        (error_count / total_requests) * 100
        if total_requests else 0
    )

    return {
        "total_requests": total_requests,
        "unique_ips": len(ip_counts),
        "error_count": error_count,
        "client_error_count": client_error_count,
        "server_error_count": server_error_count,
        "success_count": success_count,
        "error_rate": round(error_rate, 2),
        "status_counts": status_counts,
        "top_ips": ip_counts.most_common(10),
        "top_endpoints": endpoint_counts.most_common(10),
        "methods": method_counts,
    }


def generate_report(stats, malformed_lines=0):
    """Create a readable text summary report."""
    lines = [
        "=" * 55,
        "             SERVER LOG ANALYSIS REPORT",
        "=" * 55,
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        f"Total requests       : {stats['total_requests']}",
        f"Unique IP addresses  : {stats['unique_ips']}",
        f"Successful responses : {stats['success_count']}",
        f"Total error responses: {stats['error_count']}",
        f"Client errors (4xx)  : {stats['client_error_count']}",
        f"Server errors (5xx)  : {stats['server_error_count']}",
        f"Error rate           : {stats['error_rate']}%",
        f"Malformed log lines  : {malformed_lines}",
        "",
        "HTTP STATUS COUNTS",
        "-" * 30,
    ]

    for status, count in sorted(stats["status_counts"].items()):
        lines.append(f"{status}: {count}")

    lines.extend(["", "TOP IP ADDRESSES", "-" * 30])

    for ip, count in stats["top_ips"]:
        lines.append(f"{ip}: {count} requests")

    lines.extend(["", "MOST REQUESTED ENDPOINTS", "-" * 30])

    for endpoint, count in stats["top_endpoints"]:
        lines.append(f"{endpoint}: {count} requests")

    lines.extend(["", "HTTP METHODS", "-" * 30])

    for method, count in stats["methods"].most_common():
        lines.append(f"{method}: {count}")

    lines.append("\n" + "=" * 55)

    return "\n".join(lines)


if __name__ == "__main__":
    sample_path = Path(__file__).parent / "data" / "sample.log"

    records, malformed = read_log_file(sample_path)
    statistics = analyze_logs(records)

    print(generate_report(statistics, malformed))
