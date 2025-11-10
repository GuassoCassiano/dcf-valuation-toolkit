''' main.py
DCF Valuation Toolkit (V1 - MVP)

This script calculates a simple Discounted Cash Flow (DCF) valuation.

It first defines the core functions needed to calculate the
present value of future cash flows and a terminal value.

It then prompts the user to manually enter all assumptions
(e.g., initial FCF, growth rate, discount rate) and uses these
inputs to calculate and print a final intrinsic value per share.
'''

# ------------------- Core DCF Functions -------------------

def calculate_fcf(operating_cash_flow, capital_expenditures):
    """Calculates Free Cash Flow (FCF) from OCF and CapEx."""
    return operating_cash_flow - capital_expenditures

def project_fcf(starting_fcf, growth_rate, years):
    """Projects Future Cash Flows for a given number of years."""
    projected_fcfs = []
    last_fcf = starting_fcf
    
    for i in range(years):
        next_fcf = last_fcf * (1 + growth_rate)
        projected_fcfs.append(next_fcf)
        last_fcf = next_fcf
        
    return projected_fcfs

def calculate_present_value(fcf_list, discount_rate):
    """Calculates the total present value of a list of future cash flows."""
    total_pv = 0 
    
    for i, fcf_value in enumerate(fcf_list):
        year = i + 1
        pv = fcf_value / ((1 + discount_rate) ** year)
        total_pv += pv
        
    return total_pv

def calculate_terminal_value(last_fcf, perpetual_growth_rate, discount_rate, years):
    """Calculates the present value of the terminal value."""
    
    # Calculate terminal value at the end of the projection period
    projected_fcf = last_fcf * (1 + perpetual_growth_rate)
    tv = projected_fcf / (discount_rate - perpetual_growth_rate)
    
    # Discount the terminal value back to today
    pv_tv = tv / ((1 + discount_rate) ** years)
    return pv_tv

def calculate_intrinsic_value(pv_cash_flows, pv_terminal_value, shares_outstanding):
    """Calculates the final intrinsic value per share."""
    total_value = pv_cash_flows + pv_terminal_value
    intrinsic_value_per_share = total_value / shares_outstanding
    return intrinsic_value_per_share


# ------------------- Main Execution -------------------

if __name__ == "__main__":

    # --- Get User Inputs ---
    print("--- Please enter company data ---")
    ticker = input("Company Ticker (e.g., AAPL): ")
    OCF = float(input("Operating Cash Flow (in millions): "))
    CapEx = float(input("Capital Expenditures (in millions): "))

    # Calculate Free Cash Flow
    company_fcf = calculate_fcf(OCF, CapEx)
    print(f"Calculated Free Cash Flow: ${company_fcf:,.2f} million")

    # Get projection inputs
    growth_rate = float(input("Expected Growth Rate (decimal, e.g., 0.05 for 5%): "))
    years = int(input("Number of years to project (e.g., 5): "))

    # Calculate Projected Free Cash Flows
    cash_flows = project_fcf(company_fcf, growth_rate, years)
    
    # Get discount rate input
    discount_rate = float(input("Discount Rate (WACC) (decimal, e.g., 0.10 for 10%): "))

    # Calculate Present Value of Projected Cash Flows
    total_pv = calculate_present_value(cash_flows, discount_rate)
    print(f"Total Present Value of Projected Cash Flows: ${total_pv:,.2f} million")
    
    # Get perpetual growth input
    perpetual_growth_rate = float(input("Perpetual Growth Rate (decimal, e.g., 0.03 for 3%): "))

    # Calculate Present Value of Terminal Value
    pv_tv = calculate_terminal_value(cash_flows[-1], perpetual_growth_rate, discount_rate, years)
    print(f"Present Value of Terminal Value: ${pv_tv:,.2f} million")

    # Get shares input
    shares_outstanding = float(input('Shares Outstanding (in millions): '))

    # Calculate Intrinsic Value per Share
    intrinsic_value_per_share = calculate_intrinsic_value(total_pv, pv_tv, shares_outstanding)
    
    print("\n--- Final Valuation ---")
    print(f"Calculated Intrinsic Value per Share: ${intrinsic_value_per_share:,.2f}")
    print("-----------------------")

# ------------------- Save data -------------------
    # 1. Import the library
    import sqlite3
    import datetime # To get a timestamp
    
    print("\n--- Saving results to database ---")
    
    try:
        # 2. Connect to the database file (it will be created if it doesn't exist)
        conn = sqlite3.connect('valuations.db')
        cursor = conn.cursor() # 'cursor' is like your mouse, it executes commands
        
        # 3. CREATE TABLE (but only if it doesn't exist already)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dcf_results (
                ticker TEXT,
                run_date TEXT,
                ocf REAL,
                capex REAL,
                growth_rate REAL,
                discount_rate REAL,
                perp_growth_rate REAL,
                shares_outstanding REAL,
                intrinsic_value REAL
            )
        ''')
        
        # 4. INSERT INTO: Save your variables
        # We use '?' as placeholders to prevent SQL injection (a security risk)
        # This is the safest way to insert variables.
        today = str(datetime.date.today())
        data_to_insert = (
            ticker,
            today,
            OCF,
            CapEx,
            growth_rate,
            discount_rate,
            perpetual_growth_rate,
            shares_outstanding,
            intrinsic_value_per_share
        )
        
        cursor.execute('''
            INSERT INTO dcf_results VALUES (?,?, ?, ?, ?, ?, ?, ?, ?)
        ''', data_to_insert)
        
        # 5. Commit (save) the changes and close the connection
        conn.commit()
        conn.close()
        
        print("Results successfully saved to valuations.db")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")