# Utility scripts to get an overview of your PIP dependencies
I wrote these tools because unlike in the Node ecosystem, there's no way to separate packages that I installed willingly from the ones that are dependencies of others.  
Those scripts aim to give an overview of what you actually use/need, and the rest.  
You can find an example of the generated files in the [`output`](./output) folder.

## Prerequisites
- Python 3
- `pip` available in your terminal
- `matplotlib` (required by `plots.py`)

## Recommended execution order
1. `python dependency_mapper.py`
2. `python summarize.py`
3. `python gen_html.py`
4. `python plots.py`

All generated files are written in the local `output/` folder.

## `dependency_mapper.py`
Quite simple.  
`python dependency_mapper.py` will generate a `dependencies.json` file in the `output` folder, which contains a mapping of all your installed packages and their dependencies.  
Beware, it **will** take a while.

### What it does
- Reads all installed packages from `pip freeze`
- For each package, runs `pip show <package>`
- Extracts :
	- `requires` (direct dependencies)
	- `required_by` (packages depending on it)
- Saves everything into `output/dependencies.json`

### Output
- [`output/dependencies.json`](./output/dependencies.json)

## `gen_html.py`
Generates a visual dependency map as a standalone HTML file.

### What it does
- Loads `output/dependencies.json`
- Groups packages by number of dependents (`required_by` count)
- Places package boxes in rows/layers
- Draws connectors/arrows from package to its dependencies
- Applies layer-based coloring for easier visual scanning
- Allows to search packages by name and reorder them based on the depth of their dependency tree
- Click-to-drag
- Hover over a package to see its dependencies and dependents, click on it to select it
- Dark mode toggle

### Usage
`python gen_html.py`, then `python -m http.server` and open `http://localhost:8000/output/dependencies.html` in your browser, or just open the `output/dependencies.html` file directly in your browser.

### Output
- [`output/dependencies.html`](./output/dependencies.html)

## `plots.py`
Creates multiple Matplotlib charts from `output/dependencies.json`.

### Usage
`python plots.py`

### Generated plots
- [`output/requires_distribution.png`](./output/requires_distribution.png)  
	Histogram of number of direct dependencies (`requires`) per package
- [`output/required_by_distribution.png`](./output/required_by_distribution.png)  
	Histogram of number of dependents (`required_by`) per package
- [`output/top_dependents.png`](./output/top_dependents.png)  
	Horizontal bar chart of top packages by dependent count
- [`output/requires_vs_required_by_scatter.png`](./output/requires_vs_required_by_scatter.png)  
	Scatter plot comparing `requires` vs `required_by`
- [`output/pie_top_requires.png`](./output/pie_top_requires.png)  
	Pie chart of top packages by `requires` (+ Others)
- [`output/pie_top_required_by.png`](./output/pie_top_required_by.png)  
	Pie chart of top packages by `required_by` (+ Others)
- [`output/pie_zero_requires.png`](./output/pie_zero_requires.png)  
	Pie chart: packages with zero requires vs non-zero requires
- [`output/bar_avg_requires.png`](./output/bar_avg_requires.png)  
	Bar chart of average `requires` grouped by dependent count buckets
- [`output/cumulative_dependents.png`](./output/cumulative_dependents.png)  
	Cumulative distribution curve of dependents

## `summarize.py`
Prints a quick textual summary of the dependency map.

### Usage
`python summarize.py`

### What it prints
- Packages required by no other package
- Package(s) with the highest number of dependents
- Package(s) with the highest number of direct dependencies

## Notes
- `summarize.py`, `gen_html.py`, and `plots.py` all expect `output/dependencies.json` to already exist
- If you are using multiple Python environments, run these scripts inside the environment you want to analyze
