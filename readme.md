##Steps for setup 
#### Create a venv using python -m venv venv
#### Install dependencies using 

```python
pip install -r requirements.txt
```

### 1. Enable Imap from your gmail settings
### 2. Create conf dir in root inside that create credentials.py with following format
```python
email_address = '<email>'
email_password = '<app password>'
imap_url = 'imap.gmail.com'
```
### 3. Create a output dir in root 
### 4. Create a Attachments dir in root 
### 5. Update the searchEmail parameter in code
### 6. Run the code using
```python
python app.py
```

