#! /bin/bash

pip install twine
pip install build
pip install wheel
python -m build --sdist
python -m build --wheel
twine check dist/* && twine upload dist/*