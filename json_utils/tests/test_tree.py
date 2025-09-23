import json_utils
import numpy
import tempfile
import os


def test_tree_empty_dir():
    with tempfile.TemporaryDirectory() as tmp:
        r = json_utils.tree.read(tmp)
        assert len(r) == 0
        assert r == {}


def test_tree_one_file():
    with tempfile.TemporaryDirectory() as tmp:
        json_utils.write(os.path.join(tmp, "a.json"), {"1": 1, "2": 2})

        r = json_utils.tree.read(tmp)
        assert "a" in r
        assert r["a"]["1"] == 1
        assert r["a"]["2"] == 2


def _write_dummy(path, n):
    dummy = {"{:d}".format(n): n, "{:d}".format(n + 1): n + 1}
    json_utils.write(path, dummy)


def _write_dummy_list_only(path, n):
    dummy = [n, n + 1, n + 2]
    json_utils.write(path, dummy)


def _write_dummy_list_only_no_numpy(path, n):
    dummy = ["{:d}".format(n + i) for i in range(3)]
    json_utils.write(path, dummy)


def _make_dummy_tree(tmp):
    tmp_A = os.path.join(tmp, "A")
    tmp_B = os.path.join(tmp, "B")
    tmp_BR = os.path.join(tmp_B, "R")
    tmp_AD = os.path.join(tmp_A, "D")
    os.makedirs(tmp_A)
    os.makedirs(tmp_B)
    os.makedirs(tmp_BR)
    os.makedirs(tmp_AD)

    _write_dummy(os.path.join(tmp, "a.json"), 1)
    _write_dummy(os.path.join(tmp, "b.json"), 2)
    json_utils.write(os.path.join(tmp, "empty.json"), {})

    _write_dummy(os.path.join(tmp_A, "a.json"), 3)
    _write_dummy(os.path.join(tmp_A, "b.json"), 4)
    _write_dummy(os.path.join(tmp_A, "c.json"), 5)

    _write_dummy(os.path.join(tmp_AD, "a.json"), 6)
    _write_dummy(os.path.join(tmp_AD, "aa.json"), 7)
    _write_dummy(os.path.join(tmp_AD, "aaa.json"), 8)
    _write_dummy_list_only(os.path.join(tmp_AD, "lll.json"), 9)
    _write_dummy_list_only_no_numpy(
        os.path.join(tmp_AD, "lll_no_numpy.json"), 1337
    )

    # tmp_B has no json-file but a directory which contains a json-file.
    _write_dummy(os.path.join(tmp_BR, "rrr.json"), 9)


def _assert_dummy_tree(tree):
    r = tree
    assert r["a"]["1"] == 1
    assert r["a"]["2"] == 2

    assert r["b"]["2"] == 2
    assert r["b"]["3"] == 3

    assert len(r["empty"]) == 0

    assert r["A"]["a"]["3"] == 3
    assert r["A"]["a"]["4"] == 4

    assert r["A"]["b"]["4"] == 4
    assert r["A"]["b"]["5"] == 5

    assert r["A"]["c"]["5"] == 5
    assert r["A"]["c"]["6"] == 6

    assert r["A"]["D"]["a"]["6"] == 6
    assert r["A"]["D"]["a"]["7"] == 7

    assert r["A"]["D"]["a"]["6"] == 6
    assert r["A"]["D"]["a"]["7"] == 7

    assert r["A"]["D"]["aa"]["7"] == 7
    assert r["A"]["D"]["aa"]["8"] == 8

    assert r["A"]["D"]["aaa"]["8"] == 8
    assert r["A"]["D"]["aaa"]["9"] == 9

    assert r["A"]["D"]["lll"][0] == 9
    assert r["A"]["D"]["lll"][1] == 10
    assert r["A"]["D"]["lll"][2] == 11

    assert r["A"]["D"]["lll_no_numpy"][0] == "1337"
    assert r["A"]["D"]["lll_no_numpy"][1] == "1338"
    assert r["A"]["D"]["lll_no_numpy"][2] == "1339"

    assert len(r["B"]) == 1
    assert "R" in r["B"]

    assert r["B"]["R"]["rrr"]["9"] == 9
    assert r["B"]["R"]["rrr"]["10"] == 10


def _assert_dummy_dirtree(dirtree):
    assert "A" in dirtree
    assert "D" in dirtree["A"]
    assert "B" in dirtree
    assert "R" in dirtree["B"]


def test_tree_complex():
    with tempfile.TemporaryDirectory() as tmp:
        _make_dummy_tree(tmp=tmp)

        tree = json_utils.tree.read(tmp)

        _assert_dummy_tree(tree=tree)

        tree, dirtree = json_utils.tree.read_with_dirtree(path=tmp)

        _assert_dummy_tree(tree=tree)
        _assert_dummy_dirtree(dirtree=dirtree)

        tmp2 = os.path.join(tmp, "2")

        json_utils.tree.write(path=tmp2, tree=tree, dirtree=dirtree)
        tree2, dirtree2 = json_utils.tree.read_with_dirtree(path=tmp2)

        _assert_dummy_tree(tree=tree2)
        _assert_dummy_dirtree(dirtree=dirtree2)


def test_lazy_tree_complex():
    with tempfile.TemporaryDirectory() as tmp:
        _make_dummy_tree(tmp=tmp)
        tree = json_utils.tree.Tree(tmp)
        _assert_dummy_tree(tree=tree)
