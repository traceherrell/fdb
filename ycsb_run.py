import subprocess
import os
import re

metrics = [
    {
        "grep": "[OVERALL], Throughput",
        "op": "sum",
        "metric": "Throughput (ops/sec)",
        "value": 0,
    },
    {
        "grep": "[OVERALL], RunTime(ms)",
        "op": "sum",
        "metric": "Runtime (ms)",
        "value": 0,
    },
    {
        "grep": "[INSERT], Operations",
        "op": "sum",
        "metric": "OperationCountInsert",
        "value": 0,
    },
    {
        "grep": "[INSERT], Return=ERROR",
        "op": "sum",
        "metric": "ErrorCountInsert",
        "value": 0,
    },
    {
        "grep": "[INSERT], Return=OK",
        "op": "sum",
        "metric": "SuccessCountInsert",
        "value": 0,
    },
    {
        "grep": "[INSERT], Return=UNEXPECTED_STATE",
        "op": "sum",
        "metric": "UnknownCountInsert",
        "value": 0,
    },
    {
        "grep": "[INSERT], AverageLatency",
        "op": "max",
        "metric": "AverageInsertLatency",
        "value": 0,
    },
    {
        "grep": "[READ], Operations",
        "op": "sum",
        "metric": "OperationCountRead",
        "value": 0,
    },
    {
        "grep": "[READ], Return=ERROR",
        "op": "sum",
        "metric": "ErrorCountRead",
        "value": 0,
    },
    {
        "grep": "[READ], Return=OK",
        "op": "sum",
        "metric": "SuccessCountRead",
        "value": 0,
    },
    {
        "grep": "[READ], Return=UNEXPECTED_STATE",
        "op": "sum",
        "metric": "UnknownCountRead",
        "value": 0,
    },
    {
        "grep": "[READ], AverageLatency",
        "op": "max",
        "metric": "AverageReadLatency",
        "value": 0,
    },
    {
        "grep": "[READ], 95thPercentileLatency",
        "op": "max",
        "metric": "95thPercentileReadLatency",
        "value": 0,
    },
    {
        "grep": "[READ], 99thPercentileLatency",
        "op": "max",
        "metric": "99thPercentileReadLatency",
        "value": 0,
    },
    {
        "grep": "[UPDATE], Operations",
        "op": "sum",
        "metric": "OperationCountUpdate",
        "value": 0,
    },
    {
        "grep": "[UPDATE], Return=ERROR",
        "op": "sum",
        "metric": "ErrorCountUpdate",
        "value": 0,
    },
    {
        "grep": "[UPDATE], Return=OK",
        "op": "sum",
        "metric": "SuccessCountUpdate",
        "value": 0,
    },
    {
        "grep": "[UPDATE], Return=UNEXPECTED_STATE",
        "op": "sum",
        "metric": "UnknownCountUpdate",
        "value": 0,
    },
    {
        "grep": "[UPDATE], AverageLatency",
        "op": "max",
        "metric": "AverageUpdateLatency",
        "value": 0,
    },
    {
        "grep": "[UPDATE], 95thPercentileLatency",
        "op": "max",
        "metric": "95thPercentileUpdateLatency",
        "value": 0,
    },
    {
        "grep": "[UPDATE], 99thPercentileLatency",
        "op": "max",
        "metric": "99thPercentileUpdateLatency",
        "value": 0,
    },
]


def parse_log(log):
    # loop though each line in the log
    for line in log.splitlines():
        # if we find the line with the grep, parse it and update the metric
        for metric in metrics:
            if metric["grep"] in line:
                match = re.search(r"\d+", line)
                if match:
                    value = int(match.group(0))
                    if metric["op"] == "sum":
                        metric["value"] += value
                    elif metric["op"] == "max":
                        if value > metric["value"]:
                            metric["value"] = value
                    else:
                        print("Unknown operation: " + metric["op"])
                        exit(1)


def get_statefulset_pods():
    pods = (
        subprocess.check_output(
            ["oc", "get", "pods", "--selector", "app=ycsb", "-o", "name"]
        )
        .decode("utf-8")
        .strip()
    )
    return pods.split()


def get_pod_logs(namespace, name):
    logs = subprocess.check_output(["oc", "logs", "-n", namespace, name]).decode(
        "utf-8"
    )
    return logs


def aggregate_statefulset_logs(namespace, name):
    pods = get_statefulset_pods()

    log_file = "statefulset-logs.txt"

    if os.path.exists(log_file):
        os.remove(log_file)

    with open(log_file, "w") as f:
        for pod in pods:
            log = get_pod_logs(namespace, pod)
            parse_log(log)
            f.write(log)


if __name__ == "__main__":
    namespace = "default"
    name = "ycsb"

    aggregate_statefulset_logs(namespace, name)

    for metric in metrics:
        print(metric["metric"] + ": " + str(metric["value"]))
