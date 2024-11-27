# Similar Rank Traffic Estimator

A Python script that estimates website traffic using the SimilarWeb API. The script processes a list of URLs from a text or CSV file and generates traffic estimates based on SimilarWeb ranking data.

## Features

- Processes URLs from both TXT and CSV files
- Estimates traffic ranges based on SimilarWeb ranking
- Handles various error cases (rate limiting, timeouts, etc.)
- Outputs results in CSV format with clear traffic range estimates

## Prerequisites

- Python 3.7+
- SimilarWeb API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add your SimilarWeb API key:
```
SIMILARWEB_API_KEY=your_api_key_here
```

## Usage

1. Prepare your input file (either .txt or .csv) with one URL per line.

2. Run the script:
```bash
python similar_rank_traffic_estimator.py input_file.txt
```

The script will generate a `traffic_estimates.csv` file with the following columns:
- url
- similar_rank
- low_range_traffic_estimate
- high_range_traffic_estimate

## Error Handling

The script handles various error cases:
- Rate limiting (429)
- Not found (404)
- Timeouts
- General API errors
- Missing API key

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch:
    ```bash
    git checkout -b feature/AmazingFeature
    ```

3. Commit your changes:
    ```bash
    git commit -m 'Add some AmazingFeature'
    ```

4. Push to the branch:
    ```bash
    git push origin feature/AmazingFeature
    ```

5. Open a Pull Request

## License

MIT License

Copyright (c) 2024 Robert Li

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.