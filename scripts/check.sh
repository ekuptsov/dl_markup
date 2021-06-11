echo "flake8:" && flake8 --config=.flake8 dl_markup
echo "pydocstyle:" && pydocstyle --config=.pydocstyle dl_markup
pytest .