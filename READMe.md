# 🕵️‍♂️ Serverless Email Tracker (AWS Lambda + DynamoDB)

> **"Chrome Extensions are trash."** > Why install a heavy, privacy-invading browser extension just to see if someone read your email? Most free trackers sell your data or insert "Sent with X Tracker" signatures into your emails. 

This project is a **100% Free, DIY, Invisible** alternative built on AWS. It allows you to track email opens manually without anyone knowing.

## 💸 Cost Analysis
This project runs entirely on the **AWS Free Tier**.
* **AWS Lambda:** Free for 400,000 GB-seconds per month (Forever).
* **DynamoDB:** 25 GB of storage free (Forever).
* **API Gateway:** 1 Million calls free (First 12 months).

**"What if I don't have Free Tier?"**
Even without the free tier, the cost is negligible.
* **10,000 tracked emails** would cost approximately **$0.02 (2 cents)** per month.
* Unless you are sending millions of emails, this is effectively free forever.

## 🚀 Features
* **Serverless:** No servers to manage. Python code runs only when an email is opened.
* **Smart Cooldown:** If a user opens the email 5 times in 1 minute, it only logs once. It waits 5 minutes before logging the same IP again.
* **Bot Filtering:** Includes logic to detect test modes.
* **Self-Blocking:** Built-in support to ignore your own IP address (e.g., School or Home Wi-Fi).

---

## 🛠️ Step-by-Step Setup Guide

### Step 1: Create the Database
1. Go to the **AWS Console** and search for **DynamoDB**.
2. Click **Create table**.
3. **Table name:** `EmailTrackerTable`
4. **Partition key:** `email_id` (String)
5. **Sort key:** `timestamp` (String)
6. Click **Create table**.

### Step 2: Create the Function
1. Search for **Lambda** and click **Create function**.
2. Select **Author from scratch**.
   * **Function name:** `EmailTrackerPixel`
   * **Runtime:** `Python 3.x`
3. Paste the code from `lambda_function.py` (in this repo) into the code editor.
4. **IMPORTANT:** Give your Lambda permission to write to the database:
   * Go to **Configuration** > **Permissions**.
   * Click the Role Name -> **Add permissions** -> **Attach policies**.
   * Search for `AmazonDynamoDBFullAccess` and attach it.

### Step 3: Create the Public Link (API Gateway)
1. In your Lambda function overview, click **+ Add trigger**.
2. Select **API Gateway**.
3. **Intent:** Create a new API.
4. **API Type:** HTTP API.
5. **Security:** Open (Public).
6. Click **Add**.
7. Copy your **API Endpoint URL** (It looks like `https://xyz...amazonaws.com/default/EmailTrackerPixel`).

---

## 📝 How to Use It
Insert this HTML line at the very bottom of your email source code (Roundcube, Outlook Web, etc.):

```html
<img src="https://YOUR_AWS_URL_HERE?id=Job_Application_Google&r=999" width="1" height="1" style="display:none !important;" />
```

## Parameters explained:
### id=...: The unique name for this email (so you know which one was opened).

### r=...: A random number (e.g., 123, 999) to force the browser to reload the image.

### test=true: Add this to the end (&test=true) if you are opening it yourself and don't want it counted.

## ⚙️ Advanced Customization
### Blocking Your School/Work IP
### If you often check your sent folder from a specific location (like a university campus), you can block that IP range so you don't trigger false positives.

### In lambda_function.py, find the Blocking Logic section and uncomment this lines:

```python
# if ip_address.startswith('139.179'):  # Example: Bilkent University IP
#     return return_pixel()
Changing Cooldown Time
Currently set to 300 seconds (5 minutes). To change this, modify the line:
```

### if difference < 300: 
## 🤖 Credits
### All codes and documentation in this repository were written by Google Gemini.
