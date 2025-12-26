# web-review-scaraper
# SaaS Review Scraper

A powerful Python script to scrape product reviews from G2, Capterra, and GetApp. Automate review collection for market analysis, competitive research, and product feedback aggregation.

## 🌟 Features

- **Multi-platform support**: Scrape from G2, Capterra, and GetApp
- **Date range filtering**: Collect reviews within specific time periods
- **JSON export**: Structured output for easy analysis and integration
- **Error handling**: Graceful handling of network issues and invalid inputs
- **Pagination support**: Automatically traverse multiple pages of reviews
- **Rate limiting**: Respectful scraping with built-in delays
- **Clean code**: Well-commented, modular, and maintainable

## 📋 Requirements

- Python 3.10 or higher
- Internet connection

## 🚀 Quick Start

### 1. Clone and Setup


### 2. Basic Usage


## 📖 Usage Guide

### Basic Syntax

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--company` | ✅ Yes | Product name or slug (e.g., "hubspot") |
| `--start-date` | ✅ Yes | Start date (YYYY-MM-DD or "Month DD, YYYY") |
| `--end-date` | ✅ Yes | End date (YYYY-MM-DD or "Month DD, YYYY") |
| `--source` | ✅ Yes | Source: `g2`, `capterra`, or `getapp` |
| `--output` | ❌ No | Custom output filename |

### Examples


## ⚠️ Troubleshooting

### No reviews found
- Verify company slug on the website
- Try broader date range
- Check if product exists on platform

### Date parsing error
Use format: `2024-06-15` or `June 15, 2024`

### Website blocked
- Built-in 2-second delays between requests
- Wait 5 minutes if rate limited

## 🤝 Contributing

See CONTRIBUTING.md for guidelines.

## 📄 License

MIT License - see LICENSE file

---

**Made with ❤️ for competitive programmers**
