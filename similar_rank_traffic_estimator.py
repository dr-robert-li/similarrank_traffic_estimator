import os
import csv
import sys
import requests
from typing import Dict, List, Tuple
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

def clean_url(url: str) -> str:
    """Extract and clean domain from URL."""
    # Parse the URL
    parsed = urlparse(url)
    # Get the netloc (domain) part
    domain = parsed.netloc if parsed.netloc else parsed.path
    # Remove 'www.' if present
    domain = domain.replace('www.', '')
    return domain

def get_traffic_estimate(rank: int) -> Tuple[str, str]:
    """Return tuple of (low_estimate, high_estimate) based on rank."""
    if rank <= 1000:
        return ("20M", "∞")
    elif rank <= 2500:
        return ("10M", "20M")
    elif rank <= 5000:
        return ("5M", "10M")
    elif rank <= 10000:
        return ("2M", "5M")
    elif rank <= 20000:
        return ("1M", "2M")
    elif rank <= 50000:
        return ("500K", "1M")
    elif rank <= 100000:
        return ("200K", "500K")
    elif rank <= 250000:
        return ("100K", "200K")
    elif rank <= 500000:
        return ("50K", "100K")
    elif rank <= 1000000:
        return ("20K", "50K")
    elif rank <= 1500000:
        return ("10K", "20K")
    elif rank <= 2000000:
        return ("5K", "10K")
    elif rank <= 5000000:
        return ("2K", "5K")
    elif rank <= 10000000:
        return ("1K", "2K")
    else:
        return ("0", "1K")

def process_url(url: str, api_key: str) -> Dict:
    """Process a single URL and return its traffic data."""
    print(f"\n===> Analyzing: {url}")
    clean_domain = clean_url(url)
    result = {
        "url": url,
        "similar_rank": "N/A",
        "low_range_traffic_estimate": "N/A",
        "high_range_traffic_estimate": "N/A"
    }

    try:
        print("Fetching SimilarWeb rank data...")
        response = requests.get(
            f"https://api.similarweb.com/v1/similar-rank/{clean_domain}/rank",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            params={"api_key": api_key},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            rank = data.get('similar_rank', {}).get('rank')
            if rank:
                low_estimate, high_estimate = get_traffic_estimate(int(rank))
                result.update({
                    "similar_rank": rank,
                    "low_range_traffic_estimate": low_estimate,
                    "high_range_traffic_estimate": high_estimate
                })
                print(f"Rank: {rank}")
                print(f"Estimated Traffic Range: {low_estimate} - {high_estimate} visits per month")
        elif response.status_code == 429:
            print("Error: Rate limit exceeded")
            result.update({
                "similar_rank": "RATE_LIMITED",
                "low_range_traffic_estimate": "RATE_LIMITED",
                "high_range_traffic_estimate": "RATE_LIMITED"
            })
        elif response.status_code == 404:
            print("Error: Domain not found")
            result.update({
                "similar_rank": "NOT_FOUND",
                "low_range_traffic_estimate": "NOT_FOUND",
                "high_range_traffic_estimate": "NOT_FOUND"
            })
        else:
            print(f"Error: API returned status code {response.status_code}")
            result.update({
                "similar_rank": f"ERROR_{response.status_code}",
                "low_range_traffic_estimate": f"ERROR_{response.status_code}",
                "high_range_traffic_estimate": f"ERROR_{response.status_code}"
            })
    except requests.exceptions.Timeout:
        print("Error: Request timed out")
        result.update({
            "similar_rank": "TIMEOUT",
            "low_range_traffic_estimate": "TIMEOUT",
            "high_range_traffic_estimate": "TIMEOUT"
        })
    except Exception as e:
        print(f"Error: {str(e)[:30]}")
        result.update({
            "similar_rank": f"ERROR_{str(e)[:30]}",
            "low_range_traffic_estimate": "ERROR",
            "high_range_traffic_estimate": "ERROR"
        })

    return result

def main():
    api_key = os.getenv('SIMILARWEB_API_KEY')
    if not api_key:
        print("Error: SIMILARWEB_API_KEY not found in .env file")
        sys.exit(1)

    if len(sys.argv) != 2:
        print("Usage: python similar_rank_traffic_estimator.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found")
        sys.exit(1)

    urls = []
    # Handle both CSV and TXT files
    if input_file.endswith('.csv'):
        with open(input_file, 'r') as f:
            reader = csv.reader(f)
            urls = [row[0] for row in reader]
    else:
        with open(input_file, 'r') as f:
            urls = [line.strip() for line in f if line.strip()]

    total_urls = len(urls)
    print(f"\nProcessing {total_urls} URLs...")
    
    output_file = 'traffic_estimates.csv'
    fieldnames = ['url', 'similar_rank', 'low_range_traffic_estimate', 'high_range_traffic_estimate']
    
    # Track statistics
    stats = {
        'success': 0,
        'not_found': 0,
        'rate_limited': 0,
        'errors': 0,
        'timeouts': 0
    }

    # Create file and write header
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

    # Process URLs and write results immediately
    for index, url in enumerate(urls, 1):
        print(f"\nURL {index}/{total_urls}")
        print("=" * 50)
        result = process_url(url, api_key)
        
        # Update statistics
        if result['similar_rank'] == 'NOT_FOUND':
            stats['not_found'] += 1
        elif result['similar_rank'] == 'RATE_LIMITED':
            stats['rate_limited'] += 1
        elif result['similar_rank'] == 'TIMEOUT':
            stats['timeouts'] += 1
        elif 'ERROR' in str(result['similar_rank']):
            stats['errors'] += 1
        else:
            stats['success'] += 1

        # Append result to CSV
        with open(output_file, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow(result)
        print("=" * 50)
    
    # Print summary
    print("\nAnalysis Summary:")
    print("=" * 50)
    print(f"Total URLs processed: {total_urls}")
    print(f"Successful lookups: {stats['success']}")
    print(f"Domains not found: {stats['not_found']}")
    print(f"Rate limit hits: {stats['rate_limited']}")
    print(f"Timeouts: {stats['timeouts']}")
    print(f"Other errors: {stats['errors']}")
    print("=" * 50)
    print(f"\nResults written to {output_file}")

if __name__ == "__main__":
    main()