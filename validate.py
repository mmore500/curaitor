#!/bin/env python

import pathlib

import curaitor

if __name__ == "__main__":
    print("loaded", curaitor)

    print("TODO download source PDFs")

    prompt = "My LLM prompt here."

    print(f"TODO call pipeline with {prompt=}")

    print("TODO load expected output")

    print("TODO calculate and log performance")

    print("TODO save data output")
    pathlib.Path("output.txt").touch()
