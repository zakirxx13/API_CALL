#!/usr/bin/env python3
"""
Toffee Live Content Scraper
Runs via GitHub Actions
"""

import requests
import json
import os
from datetime import datetime

class ToffeeScraper:
    def __init__(self):
        self.content_api = "https://content-prod.services.toffeelive.com"
        self.entitlement_api = "https://entitlement-prod.services.toffeelive.com"
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Origin': 'https://toffeelive.com',
            'Referer': 'https://toffeelive.com/'
        })
        
        self.region = "BD"
        self.city = "DK"
    
    def fetch_rail(self, rail_id):
        """Fetch single content rail"""
        url = f"{self.content_api}/toffee/{self.region}/{self.city}/web/rail/generic/editorial-dynamic/{rail_id}"
        try:
            resp = self.session.get(url, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"Rail {rail_id} failed: {e}")
            return None
    
    def fetch_playback(self, content_id):
        """Fetch playback info"""
        url = f"{self.entitlement_api}/toffee/{self.region}/{self.city}/web/playback/{content_id}"
        try:
            resp = self.session.get(url, timeout=30)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"Playback {content_id} failed: {e}")
            return None
    
    def scrape_all(self):
        """Main scrape function"""
        rail_ids = [
            "cceb01a3ecb01516539b0adad38c1400",
            "08d90cecf964eb9a5f6be2e1887066fd",
            "55fdb2bedaca2de399b470fb0ce14117",
            "911e8f640af3a8892b628714d4acc133",
            "84a2451df95d2eb3d2b0d09c5fc34fb1",
            "9988b22058e87ba742a8d734e640e759",
            "be7d42854f019db42fbc22153674b888",
            "36eff4e5ed817e63c4a0859a0e11f1d5",
            "cb7ea308e7742680ea8df1aae153bc9b"
        ]
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "rails": []
        }
        
        for rail_id in rail_ids:
            print(f"Fetching: {rail_id}")
            data = self.fetch_rail(rail_id)
            if data:
                results["rails"].append({
                    "rail_id": rail_id,
                    "data": data
                })
        
        return results
    
    def save(self, data, folder="data"):
        """Save to JSON file"""
        os.makedirs(folder, exist_ok=True)
        filename = f"{folder}/toffeelive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Saved: {filename}")
        return filename


def main():
    scraper = ToffeeScraper()
    data = scraper.scrape_all()
    scraper.save(data)
    print("Scrape complete!")

if __name__ == "__main__":
    main()
