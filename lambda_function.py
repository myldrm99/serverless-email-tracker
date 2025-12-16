import json
import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('EmailTrackerTable')

def lambda_handler(event, context):
    query_params = event.get('queryStringParameters') or {}
    headers = event.get('headers') or {}
    
    email_id = query_params.get('id', 'unknown')
    # Get the REAL IP address (handles proxies)
    ip_address = headers.get('x-forwarded-for', 'unknown').split(',')[0].strip()
    user_agent = headers.get('user-agent', 'unknown')

    # --- 1. BLOCKING LOGIC ---
    
    # A. Block Manual Test Link
    # Add '&test=true' to your URL to prevent logging your own visits
    if query_params.get('test') == 'true':
        print(f"IGNORED: Manual Test Link for {email_id}")
        return return_pixel()

    # B. Block Specific IPs (Optional)
    # Uncomment the lines below to block your own Home/School IP
    # if ip_address.startswith('192.168.1.1'): 
    #     print(f"IGNORED: Blocked IP Access: {ip_address}")
    #     return return_pixel()

    # --- 2. IP-BASED COOLDOWN ---
    # Prevents the same user from spamming the logs (5 Minute Cooldown)
    try:
        # Get the last 20 opens for this email
        response = table.query(
            KeyConditionExpression=Key('email_id').eq(email_id),
            ScanIndexForward=False, 
            Limit=20 
        )

        # Check if THIS IP has opened it recently
        for item in response.get('Items', []):
            if item['ip_address'] == ip_address:
                last_time = datetime.fromisoformat(item['timestamp'])
                difference = (datetime.utcnow() - last_time).total_seconds()
                
                if difference < 300: # 300 seconds = 5 Minutes
                    print(f"COOLDOWN: IP {ip_address} is waiting.")
                    return return_pixel()
                break 

    except Exception as e:
        print(f"Error checking cooldown: {e}")

    # --- 3. LOGGING ---
    try:
        now = datetime.utcnow().isoformat()
        table.put_item(Item={
            'email_id': email_id,
            'timestamp': now,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'city': headers.get('cloudfront-viewer-country', 'unknown')
        })
        print(f"SUCCESS: Logged open for {email_id}")
        
    except Exception as e:
        print(f"Error saving to DB: {e}")

    return return_pixel()

def return_pixel():
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "image/gif",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0"
        },
        "body": "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7",
        "isBase64Encoded": True
    }
