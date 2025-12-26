#!/usr/bin/env python3
"""
Main entry point for the SaaS Review Scraper.

This script allows users to scrape product reviews from multiple SaaS review platforms
(G2, Capterra, GetApp) and export them as JSON files.
"""

import argparse
import sys
from g2_scraper import get_g2_reviews
from capterra_scraper import get_capterra_reviews
from getapp_scraper import get_getapp_reviews
from utils import validate_inputs, save_to_json, print_summary


def main():
    """
    Main function: parse arguments, validate, scrape, and save reviews.
    
    Flow:
    1. Parse command-line arguments
    2. Validate inputs
    3. Call appropriate scraper based on source
    4. Save results to JSON file
    5. Print summary
    """
    
    parser = argparse.ArgumentParser(
        description="Scrape SaaS product reviews from G2, Capterra, and GetApp.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scraper.py --company hubspot --start-date 2024-01-01 --end-date 2024-12-31 --source g2
  python scraper.py --company salesforce --start-date "January 1, 2024" --end-date "December 31, 2024" --source capterra --output my_file.json
  python scraper.py --company asana --start-date 2024-06-01 --end-date 2024-06-30 --source getapp

Supported date formats:
  - YYYY-MM-DD (e.g., 2024-01-15)
  - Month DD, YYYY (e.g., January 15, 2024)
  - MM/DD/YYYY (e.g., 01/15/2024)
        """
    )
    
    parser.add_argument(
        '--company',
        required=True,
        metavar='COMPANY',
        help='Company name or product slug (e.g., "hubspot", "salesforce", "asana")'
    )
    
    parser.add_argument(
        '--start-date',
        required=True,
        metavar='DATE',
        help='Start date for review period (e.g., "2024-01-01" or "January 1, 2024")'
    )
    
    parser.add_argument(
        '--end-date',
        required=True,
        metavar='DATE',
        help='End date for review period (e.g., "2024-12-31" or "December 31, 2024")'
    )
    
    parser.add_argument(
        '--source',
        required=True,
        metavar='SOURCE',
        choices=['g2', 'capterra', 'getapp'],
        help='Review source (options: g2, capterra, getapp)'
    )
    
    parser.add_argument(
        '--output',
        default=None,
        metavar='FILE',
        help='Output JSON filename (auto-generated if not provided)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output for debugging'
    )
    
    args = parser.parse_args()
    
    try:
        print("\n" + "="*50)
        print("SaaS REVIEW SCRAPER")
        print("="*50)
        print("\n🔧 Validating inputs...", end=" ")
        
        company, start_date, end_date, source = validate_inputs(
            args.company,
            args.start_date,
            args.end_date,
            args.source
        )
        
        print("✓ Valid\n")
        
        if args.output:
            output_file = args.output
        else:
            output_file = f"{company}_{source}_reviews_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.json"
        
        print("-" * 50)
        
        if source == 'g2':
            reviews = get_g2_reviews(company, start_date, end_date)
        elif source == 'capterra':
            reviews = get_capterra_reviews(company, start_date, end_date)
        elif source == 'getapp':
            reviews = get_getapp_reviews(company, start_date, end_date)
        else:
            print("❌ Invalid source. This should not happen.")
            sys.exit(1)
        
        print("-" * 50)
        
        if not reviews:
            print(f"\n⚠️  Warning: No reviews found for '{company}' from {start_date.date()} to {end_date.date()}.")
            print("    This could mean:")
            print("    - The company slug is incorrect")
            print("    - The date range is outside available reviews")
            print("    - The website structure has changed")
            sys.exit(0)
        
        save_to_json(reviews, output_file)
        print_summary(company, source, start_date, end_date, len(reviews), output_file)
    
    except ValueError as e:
        print(f"\n{e}")
        sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user.")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
