import pathlib


def test_specific() -> None:  # noqa: AAA01
    assert 1 + 1 == 2


def test_multi_line_args_specific(  # noqa: AAA01
    tmp_path: pathlib.Path,
    *args,
    **kwargs,
) -> None:
    assert 1 + 1 == 2
