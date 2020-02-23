# subchk

subchk is a Python3 Script SubDomain Checker Http & Https

### Features 
- can use threading
- Get URL after  Redirect 
- autosave when catch Live URL
- No Repeated In the  saved File

```bash
git clone https://github.com/badr-azeez/subchk.git
pip install requests argparse
```

## Usage

```python
python3 subchk.py [-h] -s SUBDOMAINS [-t TIMEOUT] [-o OUTPUT]
python3 subchk.py -s subdomain.txt 
python3 subchk.py -s subdomain.txt -t 5  -o output/live.txt 
