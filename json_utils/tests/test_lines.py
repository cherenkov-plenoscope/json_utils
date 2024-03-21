import json_utils
import numpy
import tempfile
import os


def test_empty():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "a.jsonl")
        json_utils.lines.write(path, [])
        back = json_utils.lines.read(path)
        assert len(back) == 0


def test_list_of_ints():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "a.jsonl")
        json_utils.write(path, [1, 2, 3])
        back = json_utils.read(path)
        assert len(back) == 3


def test_mixed_dict_and_int():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "a.jsonl")
        json_utils.lines.write(path, [{}, 1, {}, 2])
        back = json_utils.lines.read(path)
        assert len(back) == 4
        assert isinstance(back[0], dict)
        assert back[1] == 1
        assert isinstance(back[2], dict)
        assert back[3] == 2


def test_context_manager():
    for mode in ["t", "", "|gz", "t|gz"]:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "test.jsonl")
            if "gz" in mode:
                path += ".gz"

            with json_utils.lines.open(path, "w" + mode) as jl:
                for i in range(100):
                    jl.write({"num": i})

            with json_utils.lines.open(path, "r" + mode) as jl:
                for num, obj in enumerate(jl):
                    assert num == obj["num"]
