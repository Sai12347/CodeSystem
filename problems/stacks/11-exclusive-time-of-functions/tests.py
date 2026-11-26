import random


def visible():
    return [
        {
            "in": {
                "n": 2,
                "logs": ["0:start:0", "1:start:2", "1:end:5", "0:end:6"],
            }
        },
        {
            "in": {
                "n": 1,
                "logs": [
                    "0:start:0",
                    "0:start:2",
                    "0:end:5",
                    "0:start:6",
                    "0:end:6",
                    "0:end:7",
                ],
            }
        },
        {
            "in": {
                "n": 2,
                "logs": [
                    "0:start:0",
                    "0:start:2",
                    "0:end:5",
                    "1:start:6",
                    "1:end:6",
                    "0:end:7",
                ],
            }
        },
    ]


def _gen_logs(n, num_calls, rng, max_step=5, start_ts=0):
    logs = []
    stack = []
    cur_t = start_ts
    last_event = None
    started = 0
    while started < num_calls or stack:
        can_push = started < num_calls
        can_pop = len(stack) > 0
        if can_push and (not can_pop or rng.random() < 0.55):
            if last_event is not None:
                cur_t += rng.randint(1, max_step)
            fid = rng.randrange(n)
            logs.append(f"{fid}:start:{cur_t}")
            stack.append(fid)
            started += 1
            last_event = "start"
        else:
            if last_event == "start":
                cur_t += rng.randint(0, max_step)
            else:
                cur_t += rng.randint(1, max_step)
            fid = stack.pop()
            logs.append(f"{fid}:end:{cur_t}")
            last_event = "end"
    return logs


def hidden():
    tests = []

    # 1. Single function, single 1-unit call (start == end)
    tests.append({"in": {"n": 1, "logs": ["0:start:0", "0:end:0"]}})

    # 2. Idle gap between disjoint top-level calls + unused function IDs
    tests.append({
        "in": {
            "n": 4,
            "logs": [
                "1:start:10",
                "1:end:15",
                "3:start:100",
                "3:end:100",
            ],
        }
    })

    # 3. Large timestamp boundary (near 10^9)
    tests.append({
        "in": {
            "n": 2,
            "logs": [
                "0:start:0",
                "1:start:500000000",
                "1:end:750000000",
                "0:end:1000000000",
            ],
        }
    })

    # 4. Deep mutual recursion across 3 functions
    tests.append({
        "in": {
            "n": 3,
            "logs": [
                "0:start:0",
                "1:start:1",
                "2:start:2",
                "0:start:3",
                "1:start:4",
                "1:end:4",
                "0:end:5",
                "2:end:6",
                "1:end:7",
                "0:end:8",
            ],
        }
    })

    # 5. Sequential sibling calls inside a parent with zero gap between siblings
    tests.append({
        "in": {
            "n": 3,
            "logs": [
                "0:start:0",
                "1:start:1",
                "1:end:2",
                "2:start:3",
                "2:end:4",
                "1:start:5",
                "1:end:5",
                "0:end:6",
            ],
        }
    })

    # 6. Same function called recursively 5 levels deep with varying spans
    tests.append({
        "in": {
            "n": 2,
            "logs": [
                "1:start:5",
                "1:start:10",
                "1:start:12",
                "1:start:15",
                "1:start:20",
                "1:end:25",
                "1:end:30",
                "1:end:40",
                "1:end:55",
                "1:end:100",
            ],
        }
    })

    # 7. Many small 1-unit calls back-to-back
    logs7 = []
    for i in range(20):
        fid = i % 5
        logs7.append(f"{fid}:start:{i}")
        logs7.append(f"{fid}:end:{i}")
    tests.append({"in": {"n": 5, "logs": logs7}})

    # 8. Parent has zero exclusive time after child finishes? No, parent ends at child_end + 1 (at least 1 unit after)
    # Test parent with 1 unit before and 1 unit after many nested children
    tests.append({
        "in": {
            "n": 5,
            "logs": [
                "0:start:0",
                "1:start:1",
                "2:start:2",
                "2:end:10",
                "3:start:11",
                "4:start:12",
                "4:end:20",
                "3:end:21",
                "1:end:22",
                "0:end:23",
            ],
        }
    })

    # 9. Stress test: n = 100, logs.length = 500 (max constraint) random nested calls
    rng1 = random.Random(63601)
    tests.append({"in": {"n": 100, "logs": _gen_logs(100, 250, rng1, max_step=10, start_ts=0)}})

    # 10. Stress test: n = 10, logs.length = 500 deep recursion with large timestamps
    rng2 = random.Random(63602)
    tests.append({"in": {"n": 10, "logs": _gen_logs(10, 250, rng2, max_step=100000, start_ts=50000000)}})

    return tests
