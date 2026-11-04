name: Update PSX prices

on:
  workflow_dispatch:          # manual run button
  schedule:
    # Every 10 minutes, Monday–Friday (PSX hours ~9 AM–4 PM PKT = ~4–11 UTC)
    - cron: '*/10 4-11 * * 1-5'

# keep-alive: also run once daily so GitHub never auto-disables the schedule
  # (a scheduled workflow is disabled after 60 days of repo inactivity)

jobs:
  update-prices:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install deps
        run: pip install requests
      - name: Fetch latest PSX prices
        run: python update_prices.py
