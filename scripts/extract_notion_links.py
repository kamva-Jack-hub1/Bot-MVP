#!/usr/bin/env python3
import imaplib
import email
from email.header import decode_header
import re

# Gmail configuration
email_address = "kamva.assistant@gmail.com"
password = "hase cydc yrqi abzo"

def extract_notion_links():
    try:
        # Connect to Gmail
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(email_address, password)
        mail.select("inbox")
        
        # Search for Notion emails
        status, messages = mail.search(None, '(FROM "notify@mail.notion.so")')
        email_ids = messages[0].split()
        
        print(f"📧 Found {len(email_ids)} Notion emails")
        print("=" * 50)
        
        notion_links = []
        
        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Decode subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    
                    print(f"\n📋 Email Subject: {subject}")
                    print(f"📅 Date: {msg.get('Date')}")
                    
                    # Extract body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()
                    
                    # Look for Notion links
                    notion_patterns = [
                        r'https://www\.notion\.so/[^\s<>"\']+',
                        r'https://notion\.so/[^\s<>"\']+',
                        r'View in Notion[^:]*:\s*([^\s<>"\']+)',
                        r'Open in Notion[^:]*:\s*([^\s<>"\']+)'
                    ]
                    
                    for pattern in notion_patterns:
                        matches = re.findall(pattern, body, re.IGNORECASE)
                        for match in matches:
                            if "notion.so" in match:
                                print(f"🔗 Found Notion link: {match}")
                                notion_links.append({
                                    "subject": subject,
                                    "link": match,
                                    "date": msg.get("Date")
                                })
                    
                    # Also look for point 7 references
                    if "point 7" in body.lower() or "point7" in body.lower():
                        print("🎯 Found reference to 'point 7' in email body")
                        # Extract context around point 7
                        point7_context = re.findall(r'.{0,100}point\s*7.{0,100}', body, re.IGNORECASE)
                        for context in point7_context:
                            print(f"   Context: {context.strip()}")
        
        mail.logout()
        
        if notion_links:
            print(f"\n✅ Extracted {len(notion_links)} Notion links")
            return notion_links
        else:
            print("\n❌ No Notion links found in email bodies")
            print("Note: Links might be in HTML format or require different extraction")
            return []
            
    except Exception as e:
        print(f"❌ Error extracting links: {e}")
        return []

if __name__ == "__main__":
    extract_notion_links()
