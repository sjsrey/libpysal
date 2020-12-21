""" The :mod:`libpysal.examples` module includes a number of small built-in
    example datasets as well as functions to fetch larger datasets.
"""

from typing import Union
from .base import example_manager, Example
from .builtin import datasets as builtin_datasets
from .catalog import remotes

remote_datasets = {}
for remote in remotes:
    dataset = remotes[remote]
    example = Example(
        dataset["name"],
        dataset["description"],
        dataset["n"],
        dataset["k"],
        dataset["download_url"],
        dataset["explain_url"],
    )
    remote_datasets[dataset["name"]] = example

__all__ = ["get_path", "available", "explain", "fetch_all"]

example_manager.add_examples(remote_datasets)
example_manager.add_examples(builtin_datasets)


def available() -> str:
    """List available datasets."""

    return example_manager.available()


def explain(name: str) -> str:
    """Explain a dataset by name."""

    return example_manager.explain(name)


def load_example(example_name: str) -> Union[base.Example, builtin.LocalExample]:
    """Load example dataset instance."""

    return example_manager.load(example_name)


def get_path(file_name: str) -> str:
    """Get the path for a file by searching installed datasets."""

    installed = example_manager.get_installed_names()
    for name in installed:
        example = example_manager.datasets[name]
        pth = example.get_path(file_name, verbose=False)
        if pth:
            return pth
    print("{} is not a file in any installed dataset.".format(file_name))


def download(datasets=remote_datasets):
    """
    Download all known remotes
    """

    names = list(datasets.keys())
    names.sort()
    for name in names:
        print(name)
        example = datasets[name]
        try:
            example.download()
        except:
            print("Example not downloaded: {}".format(name))


def fetch_all():
    download()
