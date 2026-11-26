import random


def visible():
    return [
        {
            "in": {
                "ops": ["FileSystem", "ls", "mkdir", "addContentToFile", "ls", "readContentFromFile"],
                "args": [[], ["/"], ["/a/b/c"], ["/a/b/c/d", "hello"], ["/"], ["/a/b/c/d"]],
            }
        },
        {
            "in": {
                "ops": [
                    "FileSystem", "mkdir", "mkdir", "addContentToFile", "ls",
                    "addContentToFile", "readContentFromFile", "ls"
                ],
                "args": [
                    [], ["/z"], ["/a"], ["/m", "hi"], ["/"],
                    ["/m", " there"], ["/m"], ["/m"]
                ],
            }
        },
    ]


def hidden():
    tests = []

    # 1. Root-only files
    tests.append({
        "in": {
            "ops": [
                "FileSystem", "addContentToFile", "addContentToFile", "ls",
                "ls", "addContentToFile", "readContentFromFile", "readContentFromFile"
            ],
            "args": [
                [], ["/beta", "two"], ["/alpha", "one"], ["/"],
                ["/beta"], ["/alpha", "plus"], ["/alpha"], ["/beta"]
            ],
        }
    })

    # 2. Deep nested mkdir and ls at every level including empty leaf
    tests.append({
        "in": {
            "ops": [
                "FileSystem", "mkdir", "ls", "ls", "ls", "ls", "ls"
            ],
            "args": [
                [], ["/a/b/c/d/e/f/g"], ["/"], ["/a"], ["/a/b/c"], ["/a/b/c/d/e/f"], ["/a/b/c/d/e/f/g"]
            ],
        }
    })

    # 3. Idempotent mkdir on existing directories
    tests.append({
        "in": {
            "ops": [
                "FileSystem", "mkdir", "addContentToFile", "mkdir", "mkdir",
                "ls", "ls", "readContentFromFile"
            ],
            "args": [
                [], ["/x/y/z"], ["/x/y/file", "data"], ["/x/y"], ["/x/y/z"],
                ["/x/y"], ["/x/y/z"], ["/x/y/file"]
            ],
        }
    })

    # 4. Multiple appends to same file
    tests.append({
        "in": {
            "ops": [
                "FileSystem", "mkdir",
                "addContentToFile", "addContentToFile", "addContentToFile", "addContentToFile",
                "readContentFromFile", "ls"
            ],
            "args": [
                [], ["/log"],
                ["/log/app", "p1-"], ["/log/app", "p2-"], ["/log/app", "p3-"], ["/log/app", "end"],
                ["/log/app"], ["/log/app"]
            ],
        }
    })

    # 5. Same filename in different directories (isolation)
    tests.append({
        "in": {
            "ops": [
                "FileSystem", "mkdir", "mkdir", "mkdir",
                "addContentToFile", "addContentToFile", "addContentToFile",
                "readContentFromFile", "readContentFromFile", "readContentFromFile",
                "ls", "ls"
            ],
            "args": [
                [], ["/a"], ["/b"], ["/a/b"],
                ["/a/f", "in_a"], ["/b/f", "in_b"], ["/a/b/f", "in_ab"],
                ["/a/f"], ["/b/f"], ["/a/b/f"],
                ["/a"], ["/a/b"]
            ],
        }
    })

    # 6. Lexicographical sorting edge cases
    tests.append({
        "in": {
            "ops": [
                "FileSystem", "mkdir", "mkdir", "addContentToFile", "mkdir",
                "addContentToFile", "addContentToFile", "ls"
            ],
            "args": [
                [], ["/dir/ba"], ["/dir/a"], ["/dir/aa", "1"], ["/dir/z"],
                ["/dir/ab", "2"], ["/dir/b", "3"], ["/dir"]
            ],
        }
    })

    # 7. Creating nested file paths directly and listing parent directories
    tests.append({
        "in": {
            "ops": [
                "FileSystem", "mkdir", "addContentToFile", "addContentToFile",
                "ls", "ls", "ls", "readContentFromFile"
            ],
            "args": [
                [], ["/usr/local/bin"], ["/usr/local/bin/tool", "bin"], ["/usr/local/readme", "doc"],
                ["/usr"], ["/usr/local"], ["/usr/local/bin"], ["/usr/local/bin/tool"]
            ],
        }
    })

    # 8. Shared directory name prefix trap (/dir vs /dira vs /dirb)
    tests.append({
        "in": {
            "ops": [
                "FileSystem", "mkdir", "mkdir", "mkdir",
                "addContentToFile", "addContentToFile", "addContentToFile",
                "ls", "ls", "ls", "ls", "readContentFromFile"
            ],
            "args": [
                [], ["/dir/sub"], ["/dira/sub"], ["/dirb/sub"],
                ["/dir/x", "one"], ["/dira/y", "two"], ["/dirb/z", "three"],
                ["/"], ["/dir"], ["/dira"], ["/dirb"], ["/dira/y"]
            ],
        }
    })

    # 9. Deterministic random file system workload (150 ops)
    rng = random.Random(58801)
    dirs = ["/"]
    dir_set = {"/"}
    files = []
    file_set = set()
    names = ["a", "b", "c", "d", "aa", "ab", "ba", "doc", "bin", "src", "tmp", "var"]
    ops9 = ["FileSystem"]
    args9 = [[]]
    for _ in range(150):
        r = rng.random()
        if r < 0.30:
            parent = rng.choice(dirs)
            seg = rng.choice(names)
            path = f"/{seg}" if parent == "/" else f"{parent}/{seg}"
            if len(path) <= 80 and path not in file_set:
                ops9.append("mkdir")
                args9.append([path])
                if path not in dir_set:
                    dir_set.add(path)
                    dirs.append(path)
        elif r < 0.60:
            if files and rng.random() < 0.4:
                fpath = rng.choice(files)
            else:
                parent = rng.choice(dirs)
                seg = rng.choice(names)
                fpath = f"/{seg}" if parent == "/" else f"{parent}/{seg}"
            if len(fpath) <= 80 and fpath not in dir_set:
                content = "".join(rng.choice("abcdefxyz") for _ in range(rng.randint(1, 10)))
                ops9.append("addContentToFile")
                args9.append([fpath, content])
                if fpath not in file_set:
                    file_set.add(fpath)
                    files.append(fpath)
        elif r < 0.80 and files:
            ops9.append("readContentFromFile")
            args9.append([rng.choice(files)])
        else:
            target = rng.choice(files) if (files and rng.random() < 0.3) else rng.choice(dirs)
            ops9.append("ls")
            args9.append([target])
    tests.append({"in": {"ops": ops9, "args": args9}})

    # 10. Max-scale deterministic workload (290 ops)
    rng = random.Random(58802)
    dirs = ["/"]
    dir_set = {"/"}
    files = []
    file_set = set()
    names = [f"n{chr(ord('a') + i)}" for i in range(16)]
    ops10 = ["FileSystem"]
    args10 = [[]]
    for _ in range(290):
        r = rng.random()
        if r < 0.30:
            parent = rng.choice(dirs)
            segs = [rng.choice(names) for _ in range(rng.randint(1, 2))]
            cur = parent
            ok = True
            for s in segs:
                nxt = f"/{s}" if cur == "/" else f"{cur}/{s}"
                if len(nxt) > 90 or nxt in file_set:
                    ok = False
                    break
                cur = nxt
            if ok:
                ops10.append("mkdir")
                args10.append([cur])
                p = parent
                for s in segs:
                    p = f"/{s}" if p == "/" else f"{p}/{s}"
                    if p not in dir_set:
                        dir_set.add(p)
                        dirs.append(p)
        elif r < 0.60:
            if files and rng.random() < 0.45:
                fpath = rng.choice(files)
            else:
                parent = rng.choice(dirs)
                seg = rng.choice(names)
                fpath = f"/{seg}" if parent == "/" else f"{parent}/{seg}"
            if len(fpath) <= 90 and fpath not in dir_set:
                content = "".join(rng.choice("abcdefghij") for _ in range(rng.randint(1, 12)))
                ops10.append("addContentToFile")
                args10.append([fpath, content])
                if fpath not in file_set:
                    file_set.add(fpath)
                    files.append(fpath)
        elif r < 0.80 and files:
            ops10.append("readContentFromFile")
            args10.append([rng.choice(files)])
        else:
            target = rng.choice(files) if (files and rng.random() < 0.35) else rng.choice(dirs)
            ops10.append("ls")
            args10.append([target])
    tests.append({"in": {"ops": ops10, "args": args10}})

    return tests
