# Amidakuji Generator

A Python CLI tool for generating Amidakuji (Japanese ladder lottery) and outputting as PDF.

## Features

- Generate Amidakuji based on specified number of vertical lines and horizontal bars range
- Save generated Amidakuji as PDF file
- Simple operation via command line arguments

## Usage

```bash
python main.py --lines 5 --min-bars 8 --max-bars 15 --output amidakuji.pdf
```

### Options

- `--lines` / `-l`: Number of vertical lines (required)
- `--min-bars` / `--min`: Minimum number of horizontal bars (required)
- `--max-bars` / `--max`: Maximum number of horizontal bars (required)
- `--output` / `-o`: Output PDF file path (required)

## Development Environment

This project is developed using Dev Containers. When VS Code detects the `.devcontainer` folder, reopening in container will automatically set up the development environment.

### Required Tools

- Docker
- Visual Studio Code
- Dev Containers extension

## License

MIT

