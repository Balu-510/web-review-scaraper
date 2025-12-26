import requests
from bs4 import BeautifulSoup
from utils import parse_date, is_date_in_range, clean_text
import time

def get_capterra_reviews(company_slug, start_date, end_date):
    """
    Scrape reviews from Capterra for a given company.
    
    Capterra is a major SaaS and software review platform owned by Gartner.
    """
    reviews = []
    page = 1
    base_url = f"https://www.capterra.com/p/{company_slug}/reviews"
    
    print(f"\n🔍 Scraping Capterra for '{company_slug}'...")
    print(f"   Date range: {start_date.date()} to {end_date.date()}")
    
    while True:
        try:
            url = f"{base_url}?page={page}" if page > 1 else base_url
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            
            print(f"   Page {page}...", end=" ", flush=True)
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            review_elements = soup.find_all('div', class_='review-card')
            
            if not review_elements:
                review_elements = soup.find_all('div', class_='review')
            
            if not review_elements:
                print(f"No reviews found.")
                break
            
            print(f"Found {len(review_elements)} reviews.", flush=True)
            
            page_had_valid_reviews = False
            
            for element in review_elements:
                try:
                    title_elem = element.find('h3', class_='review__title')
                    if not title_elem:
                        title_elem = element.find('h3')
                    
                    body_elem = element.find('p', class_='review__body')
                    if not body_elem:
                        body_elem = element.find('p')
                    
                    date_elem = element.find('span', class_='review__date')
                    if not date_elem:
                        date_elem = element.find('span', {'data-date': True})
                    
                    if not all([title_elem, body_elem, date_elem]):
                        continue
                    
                    title_text = clean_text(title_elem.get_text())
                    body_text = clean_text(body_elem.get_text())
                    date_text = clean_text(date_elem.get_text())
                    
                    rating_elem = element.find('span', class_='rating')
                    rating_text = "N/A"
                    if rating_elem:
                        rating_text = clean_text(rating_elem.get_text())
                    
                    reviewer_elem = element.find('span', class_='reviewer-name')
                    if not reviewer_elem:
                        reviewer_elem = element.find('span', class_='reviewer')
                    reviewer_text = reviewer_elem.get_text() if reviewer_elem else "Anonymous"
                    
                    try:
                        review_date = parse_date(date_text)
                    except ValueError:
                        continue
                    
                    if not is_date_in_range(review_date, start_date, end_date):
                        if review_date < start_date and page > 1:
                            print("   (Reached reviews older than start date)")
                            break
                        continue
                    
                    page_had_valid_reviews = True
                    
                    review = {
                        "title": title_text,
                        "review": body_text,
                        "date": review_date.strftime("%Y-%m-%d"),
                        "rating": rating_text,
                        "reviewer_name": clean_text(reviewer_text),
                        "source": "Capterra",
                        "company": company_slug
                    }
                    
                    reviews.append(review)
                
                except Exception as e:
                    continue
            
            next_button = soup.find('a', {'aria-label': 'Next page'})
            if not next_button:
                next_button = soup.find('a', class_='next')
            
            if not next_button or not page_had_valid_reviews:
                print("   ✓ Reached last page.")
                break
            
            page += 1
            time.sleep(2)
        
        except requests.exceptions.Timeout:
            print(f"❌ Timeout on page {page}")
            break
        except requests.exceptions.ConnectionError:
            print(f"❌ Connection error on page {page}")
            break
        except requests.exceptions.RequestException as e:
            print(f"❌ Network error on page {page}: {e}")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            break
    
    return reviews
