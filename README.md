# CheckAlive

CheckAlive is a Python tool that allows you to check the status of URLs and find subdomains. You can check a single URL or multiple URLs from a file, and it supports outputting alive URLs to a file. Additionally, you can find subdomains for a given domain using crt.sh.

## Features

- Check if a single URL or multiple URLs are alive.
- Specify acceptable status codes for URLs.
- Output alive URLs to a file.
- Find subdomains for a given domain.
- Output subdomains to a file.

## Installation

1. Clone the repository:

    ```sh
    git clone [https://github.com/yourusername/checkalive.git](https://github.com/x21enax/CheckAlive)
    cd checkalive
    ```

2. Install the package using pip:

    ```sh
    pip install .
    ```

## Usage

### Check a Single URL

Check if a single URL is alive with the specified status codes:

```sh
checkalive -u example.com -s 200,302
```
## Check Multiple URLs from a File

Check if URLs from a file are alive and output the alive URLs to a file:
```sh
checkalive -us urls.txt -s 200,302 -o aliveurls.txt
```
## Find Subdomains

Find subdomains for a given domain and output them to a file:

```sh

checkalive -u example.com -fs -o subdomains.txt
```
## Find subdomains for a given domain and print them:

```sh

checkalive -u example.com -fs
```
## Command Line Options
```sh
    -u, --url: Single URL to check or find subdomains for.
    -us, --urls: File containing URLs to check.
    -s, --status-code: Comma-separated list of acceptable status codes (default: 200,302).
    -o, --output: File to output alive URLs or subdomains when checking multiple URLs or finding subdomains.
    -fs, --find-subdomain: Find subdomains for the provided URL.
```
## Example

### Check if a single URL is alive:

```sh

checkalive -u example.com -s 200,302
```
### Check if multiple URLs from a file are alive and save the result to aliveurls.txt:

```sh

checkalive -us urls.txt -s 200,302 -o aliveurls.txt
```
### Find subdomains for a domain and save the result to subdomains.txt:

```sh

checkalive -u example.com -fs -o subdomains.txt
```
## License

This project is licensed under the MIT License. See the LICENSE file for details.
Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
Author

X21E
