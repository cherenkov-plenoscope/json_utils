import json_utils
import numpy
import tempfile
import os


def test_simple():
    with tempfile.TemporaryDirectory() as tmp:
        original = {"1": 1, "2": 2}
        path = os.path.join(tmp, "a.json")

        json_utils.write(path, original)
        back = json_utils.read(path)

        for key in original:
            assert key in back
            assert original[key] == back[key]


def test_empty():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "a.json")
        json_utils.write(path, {})
        back = json_utils.read(path)
        assert len(back) == 0
