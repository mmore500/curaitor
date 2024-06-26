
# LLMs for Data Extraction


[![GitHub Actions Status](https://github.com/mmore500/curaitor/actions/workflows/ci.yaml/badge.svg)](https://github.com/mmore500/curaitor/actions/workflows/ci/)
[![GitHub stars](https://img.shields.io/github/stars/mmore500/curaitor.svg?style=flat-square&logo=github&label=Stars&logoColor=white)](https://github.com/mmore500/curaitor)

Schmidt OxRSE 2024 Project

-   Free software: MIT license

## Set Up Development Environment

```bash
git clone https://github.com/mmore500/curaitor.git
python3 -m venv env
source env/bin/activate
python3 -m pip install -r curaitor/requirements-dev.txt
```

We recommend using Python 3.11.
If you have Python 3.11 installed, but it is not your default Python version you can use "`python3.11`" instead of "`python3`" above. 
General guidance on managing multiple Python versions can be found [here](https://realpython.com/intro-to-pyenv/).

## Contribution Guidelines

1. Open pull request.
2. Ensure tests, styling, and linting pass locally.
   ```bash
   ./test.sh
   ./style.sh
   ./lint.sh
   ``` 
3. Ensure tests, styling, and linting pass in CI.
4. Request code review.
5. Merge.

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter).
