
import datetime
import re
from collections import defaultdict
import random

# Sample customer data
customer_database = {
    "123456789": {
        "name": "Kamal Perera",
        "account_type": "Savings",
        "balance": 150000.00,
        "status": "Active",
        "last_transaction": "2024-08-25",
        "phone": "077-1234567"
    },
    "987654321": {
        "name": "Priya Fernando",
        "account_type": "Current",
        "balance": 250000.00,
        "status": "Active",
        "last_transaction": "2024-08-26",
        "phone": "071-9876543"
    }
}

# Enhanced FAQ dataset with Sri Lankan banking context
faq_dataset = {
    "what is the interest rate for a personal loan": "Personal loan interest rates start from 12.5% per annum. Rates vary based on your credit profile.",
    "what is the interest rate for housing loan": "Housing loan rates start from 10.25% per annum for up to 25 years.",
    "how do i reset my online banking password": "Go to ntb.lk → Login → Forgot Password → Enter your username and follow SMS verification.",
    "how can i check my account balance": "Check balance via NTB Mobile App, Internet Banking, ATM, or SMS banking (*#456# from registered mobile).",
    "how do i apply for a credit card": "Apply online at ntb.lk or visit any branch. Online applications processed within 3-5 working days.",
    "what are the bank working hours": "Branches: 9:00 AM - 3:00 PM (Mon-Fri). Call Center: 24/7 at 011-2448448.",
    "what is the minimum balance for savings account": "Minimum balance is LKR 1,000 for regular savings accounts.",
    "how do i activate my debit card": "Call 011-2448448 or visit any NTB branch with your NIC and account details.",
    "what are foreign transaction charges": "Foreign transactions: 2.5% + LKR 200 service charge per transaction.",
    "how do i transfer money using slips": "Use NTB Mobile App → Payments → SLIPS → Enter beneficiary details and amount.",
    "what is ceft transfer": "CEFT allows instant transfers between banks. Fee: LKR 25 per transaction.",
    "how do i open a fixed deposit": "Visit any branch with minimum LKR 10,000. Current FD rates: 12-month: 10.25%.",
    "what documents needed for account opening": "Required: NIC, Utility bill, Initial deposit (LKR 1,000 minimum)."
}

# Enhanced team routing
team_routing = {
    "loan": "Loan Processing Desk",
    "housing_loan": "Mortgage Department", 
    "account": "Customer Service Center",
    "card": "Card Services Department",
    "fraud": "Fraud Investigation Unit",
    "investment": "Investment Advisory Desk",
    "foreign_exchange": "Foreign Exchange Desk",
    "digital_banking": "Digital Banking Support",
    "complaints": "Customer Relations Department",
    "general": "Customer Service Center"
}

# Enhanced keyword mapping
category_keywords = {
    "loan": ["loan", "emi", "interest rate", "repayment", "installment"],
    "housing_loan": ["housing loan", "mortgage", "home loan", "property loan"],
    "account": ["account", "balance", "statement", "password", "login", "savings", "current"],
    "card": ["credit card", "debit card", "card issue", "blocked card", "card activation"],
    "fraud": ["fraud", "unauthorized", "scam", "stolen", "suspicious transaction"],
    "investment": ["fixed deposit", "fd", "investment", "savings plus"],
    "foreign_exchange": ["foreign exchange", "forex", "usd", "dollar", "remittance"],
    "digital_banking": ["mobile app", "internet banking", "online", "sms banking"],
    "complaints": ["complaint", "unsatisfied", "problem", "manager"]
}

# Priority levels
priority_levels = {
    "fraud": "HIGH",
    "complaints": "HIGH", 
    "loan": "MEDIUM",
    "account": "MEDIUM",
    "card": "MEDIUM",
    "general": "LOW"
}

# Analytics tracking
query_analytics = defaultdict(int)
resolution_analytics = defaultdict(int)
total_queries = 0

# Session data
customer_authenticated = False
current_customer = None

def authenticate_customer(account_number):
    #Check if customer account exists
    global customer_authenticated, current_customer
    if account_number in customer_database:
        customer_authenticated = True
        current_customer = customer_database[account_number]
        return True
    return False

def get_account_info(query):
    #Handle account-specific queries

    if not customer_authenticated:
        return "For account information, please provide your 9-digit account number first."
    
    customer = current_customer
    query_lower = query.lower()
    
    if "balance" in query_lower:
        return f"Hello {customer['name']}, your {customer['account_type']} account balance is LKR {customer['balance']:,.2f}"
    elif "statement" in query_lower:
        return f"Last transaction: {customer['last_transaction']}. Download full statement from NTB Mobile App."
    elif "status" in query_lower:
        return f"Account status: {customer['status']}"
    
    return None

def detect_urgency(query):
    #Check if query needs immediate attention
    urgent_keywords = ["emergency", "urgent", "fraud", "stolen", "unauthorized", "blocked"]
    return any(keyword in query.lower() for keyword in urgent_keywords)

def fuzzy_match_faq(query):
    #Find best matching FAQ using word overlap
    query_words = set(query.lower().split())
    best_match = None
    best_score = 0
    
    for faq_question, answer in faq_dataset.items():
        faq_words = set(faq_question.split())
        common_words = faq_words.intersection(query_words)
        score = len(common_words) / len(faq_words) if faq_words else 0
        
        if score > best_score and score > 0.3:
            best_match = answer
            best_score = score
    
    return best_match

def get_response_time(priority):
    #Estimate response time
    times = {
        "URGENT": "Within 30 minutes",
        "HIGH": "Within 2 hours", 
        "MEDIUM": "Within 4 hours",
        "LOW": "Within 24 hours"
    }
    return times.get(priority, "Within 24 hours")

def log_query(category, resolved=True):
    #Track query statistics
    global total_queries
    query_analytics[category] += 1
    total_queries += 1
    if resolved:
        resolution_analytics[category] += 1

def show_analytics():
    #Display usage statistics
    print("\n" + "="*50)
    print("BANKING AI AGENT - ANALYTICS REPORT")
    print("="*50)
    print(f"Total Queries: {total_queries}")
    print(f"Session Time: {datetime.datetime.now().strftime('%H:%M:%S')}")
    
    print("\nQuery Distribution:")
    for category, count in query_analytics.items():
        resolved = resolution_analytics[category]
        rate = (resolved / count * 100) if count > 0 else 0
        print(f"  {category.upper()}: {count} queries ({rate:.1f}% resolved)")

def answer_or_escalate(query):
    global customer_authenticated, current_customer
    
    # Check for account number in query
    account_pattern = r'\b\d{9}\b'
    account_match = re.search(account_pattern, query)
    if account_match:
        account_num = account_match.group()
        if authenticate_customer(account_num):
            log_query("authentication", resolved=True)
            return f"Authentication successful! Welcome {current_customer['name']}. How can I help you?"
        else:
            log_query("authentication", resolved=False)
            return "Account not found. Please verify your 9-digit account number."
    
    # Handle authenticated customer account queries
    if customer_authenticated:
        account_response = get_account_info(query)
        if account_response:
            log_query("account", resolved=True)
            return f"Answer: {account_response}"
    
    # Try fuzzy FAQ matching first
    faq_answer = fuzzy_match_faq(query)
    if faq_answer:
        log_query("faq", resolved=True)
        return f"Answer: {faq_answer}"
    
    # Check exact FAQ matches (original logic)
    query_lower = query.lower()
    for faq_question, answer in faq_dataset.items():
        if faq_question in query_lower:
            log_query("faq", resolved=True)
            return f"Answer: {answer}"
    
    # Determine category for escalation
    detected_category = "general"
    for category, keywords in category_keywords.items():
        if any(k in query_lower for k in keywords):
            detected_category = category
            break
    
    # Check urgency and set priority
    is_urgent = detect_urgency(query)
    priority = priority_levels.get(detected_category, "LOW")
    if is_urgent:
        priority = "URGENT"
    
    # Generate escalation with enhanced details
    team = team_routing.get(detected_category, "Customer Service Center")
    ticket_id = f"NTB{random.randint(10000, 99999)}"
    response_time = get_response_time(priority)
    
    log_query(detected_category, resolved=False)
    
    escalation_msg = f"""Complex query escalated.
Ticket ID: {ticket_id}
Team: {team}
Priority: {priority}
Expected Response: {response_time}
Contact: 011-2448448 for urgent matters"""
    
    return escalation_msg

if __name__ == "__main__":
    print("=== Nations Trust Bank AI Agent - Enhanced Demo ===")
    print("Features: Account Integration | Smart Matching | Analytics")
    print("Try: 'balance check', 'loan rates', or use account number 123456789")
    print("Commands: 'analytics' for stats, 'exit' to quit")
    print()

    while True:
        user_query = input("Enter query: ").strip()
        
        if user_query.lower() == "exit":
            print("\nSession Summary:")
            show_analytics()
            print("Thank you for using NTB AI Agent!")
            break
        
        if user_query.lower() == "analytics":
            show_analytics()
            continue
        
        if not user_query:
            print("Please enter a valid query.")
            continue

        response = answer_or_escalate(user_query)
        print(f"{response}\n")