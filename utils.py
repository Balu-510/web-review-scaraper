import json
from datetime import datetime

def parse_date(date_string):
    """
    Convert various date formats to a standardized datetime object.
    
    Supported formats:
    - "March 15, 2024" (B d, Y)
    - "03/15/2024" (m/d/Y)
    - "2024-03-15" (Y-m-d)
    - "Mar 15, 2024" (b d, Y)
    
    Args:
        date_string: Date string in any of the supported formats
    
    Returns:
        datetime object
    
    Raises:
        ValueError: If date string doesn't match any supported format
    """
    formats = [
        "%B %d, %Y",      # March 15, 2024
        "%m/%d/%Y",       # 03/15/2024
        "%Y-%m-%d",       # 2024-03-15
        "%b %d, %Y",      # Mar 15, 2024
        "%d %B %Y",       # 15 March 2024
    ]
    
    date_string = date_string.strip()
    
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Cannot parse date: '{date_string}'. Supported formats: 'YYYY-MM-DD' or 'Month DD, YYYY'")


def is_date_in_range(review_date, start_date, end_date):
    """Check if a review_date falls between start_date and end_date (inclusive)."""
    return start_date <= review_date <= end_date


def clean_text(text):
    """Clean up text: remove extra whitespace, newlines, and special characters."""
    if not text:
        return ""
    return " ".join(text.split())


def save_to_json(reviews, filename):
    """Save a list of reviews to a JSON file with pretty formatting."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(reviews, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved {len(reviews)} reviews to '{filename}'")
    except IOError as e:
        print(f"❌ Error saving file: {e}")
        raise


def load_from_json(filename):
    """Load reviews from a JSON file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except IOError as e:
        print(f"❌ Error loading file: {e}")
        raise
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in file: {e}")
        raise


def validate_inputs(company_name, start_date_str, end_date_str, source):
    """
    Validate user inputs before scraping.
    
    Args:
        company_name: Name/slug of company
        start_date_str: Start date string
        end_date_str: End date string
        source: Review source (g2, capterra, getapp)
    
    Returns:
        Tuple: (company_name, start_date, end_date, source) - all validated
    
    Raises:
        ValueError: If any input is invalid
    """
    if not company_name or len(company_name.strip()) == 0:
        raise ValueError("❌ Company name cannot be empty!")
    
    valid_sources = ["g2", "capterra", "getapp"]
    if source.lower() not in valid_sources:
        raise ValueError(f"❌ Invalid source '{source}'. Must be one of: {', '.join(valid_sources)}")
    
    try:
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)
    except ValueError as e:
        raise ValueError(str(e))
    
    if start_date > end_date:
        raise ValueError("❌ Start date cannot be after end date!")
    
    return company_name.strip(), start_date, end_date, source.lower()


def print_summary(company, source, start_date, end_date, total_reviews, output_file):
    """Print a nicely formatted summary of scraping results."""
    print("\n" + "="*50)
    print("✅ SCRAPING COMPLETED SUCCESSFULLY")
    print("="*50)
    print(f"Company:      {company}")
    print(f"Source:       {source.upper()}")
    print(f"Date Range:   {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"Total Reviews: {total_reviews}")
    print(f"Output File:  {output_file}")
    print("="*50 + "\n")
