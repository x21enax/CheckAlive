import requests
import argparse
import sys
import signal
import os
import re

def normalize_url(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url

def check_url(url, status_codes):
    url = normalize_url(url)
    try:
        response = requests.head(url, allow_redirects=True, timeout=10)
        if response.status_code in status_codes:
            return url
        else:
            return None
    except requests.RequestException:
        return None

def check_urls_from_file(file_path, status_codes, output_file):
    try:
        with open(file_path, 'r') as file:
            urls = file.readlines()
            
        alive_urls = []
        total_urls = len(urls)
        for index, url in enumerate(urls):
            url = url.strip()
            result = check_url(url, status_codes)
            if result:
                print(f"{result} is alive with status code in {status_codes}")
                alive_urls.append(url)
            print(f"\rProgress: {((index + 1) / total_urls) * 100:.2f}%", end='')
                
        print()  # To move to the next line after progress
        if output_file:
            with open(output_file, 'w') as file:
                for alive_url in alive_urls:
                    file.write(f"{alive_url}\n")
            print(f"Alive URLs have been written to {output_file}")

    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred while checking URLs from file: {e}")

def parse_status_codes(status_codes_str):
    try:
        return [int(code) for code in status_codes_str.split(',')]
    except ValueError:
        print("Invalid status code format. Please provide a comma-separated list of integers.")
        sys.exit(1)

def find_subdomains(domain, output_file):
    domain = re.sub(r'^https?://', '', domain)  # Remove http:// or https:// if present
    url = f"https://crt.sh/?q={domain}&output=json"
    try:
        response = requests.get(url, timeout=100)
        response.raise_for_status()
        data = response.json()
        total_entries = len(data)
        subdomains = set()

        for index, entry in enumerate(data):
            if 'common_name' in entry:
                subdomains.add(entry['common_name'])
            if 'name_value' in entry:
                subdomains.update(entry['name_value'].split('\n'))
            print(f"\rProgress: {((index + 1) / total_entries) * 100:.2f}%", end='')

        print()  # To move to the next line after progress
        if output_file:
            with open(output_file, 'w') as file:
                for subdomain in subdomains:
                    file.write(f"{subdomain}\n")
            print(f"Subdomains have been written to {output_file}")
        else:
            for subdomain in subdomains:
                print(subdomain)

    except requests.RequestException as e:
        print(f"Failed to fetch subdomains for {domain}: {e}")
    except ValueError:
        print("Invalid JSON response.")
    except Exception as e:
        print(f"An error occurred while finding subdomains: {e}")

def signal_handler(signum, frame):
    username = os.getenv('USER', 'user')
    print(f"\nProcess canceled by {username}.")
    sys.exit(1)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    parser = argparse.ArgumentParser(description="Check if URLs are alive and find subdomains")
    parser.add_argument('-u', '--url', type=str, help='Single URL to check or find subdomains for')
    parser.add_argument('-us', '--urls', type=str, help='File containing URLs to check')
    parser.add_argument('-s', '--status-code', type=str, default='200,302', help='Comma-separated list of acceptable status codes (default: 200,302)')
    parser.add_argument('-o', '--output', type=str, help='File to output alive URLs or subdomains when checking multiple URLs or finding subdomains')
    parser.add_argument('-fs', '--find-subdomain', action='store_true', help='Find subdomains for the provided URL')
    
    args = parser.parse_args()
    
    status_codes = parse_status_codes(args.status_code)
    
    if args.url and args.find_subdomain:
        find_subdomains(args.url, args.output)
    elif args.url:
        result = check_url(args.url, status_codes)
        if result:
            print(f"{result} is alive with status code in {status_codes}")
        else:
            print(f"{args.url} is not alive.")
    elif args.urls:
        check_urls_from_file(args.urls, status_codes, args.output)
    else:
        print("Please provide a URL, a file containing URLs, or use the --find-subdomain option.")

if __name__ == '__main__':
    main()
