# Loan and EMI Calculator

import pandas as pd
import matplotlib.pyplot as plt


# ── 1. EMI Formula ──────────────────────────────────────────
def calculate_emi(principal, annual_rate, tenure_years):
    r = annual_rate / 12 / 100      # monthly interest rate
    n = tenure_years * 12           # total months
    emi = principal * r * (1 + r)**n / ((1 + r)**n - 1)
    return round(emi, 2)


# ── 2. Amortization Schedule ────────────────────────────────
def generate_schedule(principal, annual_rate, tenure_years):
    r = annual_rate / 12 / 100
    n = tenure_years * 12
    emi = calculate_emi(principal, annual_rate, tenure_years)

    balance = principal
    schedule = []

    for month in range(1, n + 1):
        interest = round(balance * r, 2)
        principal_paid = round(emi - interest, 2)
        balance = round(balance - principal_paid, 2)

        schedule.append({
            "Month": month,
            "EMI (Rs)": emi,
            "Principal Paid (Rs)": principal_paid,
            "Interest Paid (Rs)": interest,
            "Balance (Rs)": max(balance, 0)
        })

    return pd.DataFrame(schedule)


# ── 3. Chart ─────────────────────────────────────────────────
def plot_chart(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df["Month"], df["Balance (Rs)"], color="blue", label="Remaining Balance")
    plt.bar(df["Month"], df["Interest Paid (Rs)"], alpha=0.4, color="red", label="Interest Paid")
    plt.xlabel("Month")
    plt.ylabel("Amount (Rs)")
    plt.title("Loan Repayment Schedule")
    plt.legend()
    plt.tight_layout()
    plt.savefig("loan_chart.png")
    plt.show()
    print("Chart saved as loan_chart.png")


# ── 4. Save CSV ───────────────────────────────────────────────
def save_to_csv(df):
    df.to_csv("amortization_schedule.csv", index=False)
    print("Schedule saved to amortization_schedule.csv")


# ── 5. User Input ─────────────────────────────────────────────
def get_user_input():
    print("=" * 40)
    print("      LOAN EMI CALCULATOR")
    print("=" * 40)
    principal = float(input("Enter Loan Amount (Rs): "))
    annual_rate = float(input("Enter Annual Interest Rate (%): "))
    tenure_years = int(input("Enter Loan Tenure (in years): "))
    return principal, annual_rate, tenure_years


# ── 6. Main ───────────────────────────────────────────────────
def main():
    principal, annual_rate, tenure_years = get_user_input()

    emi = calculate_emi(principal, annual_rate, tenure_years)
    total_payment = round(emi * tenure_years * 12, 2)
    total_interest = round(total_payment - principal, 2)

    print("\n" + "=" * 40)
    print(f"  Monthly EMI    : Rs {emi}")
    print(f"  Total Payment  : Rs {total_payment}")
    print(f"  Total Interest : Rs {total_interest}")
    print("=" * 40 + "\n")

    df = generate_schedule(principal, annual_rate, tenure_years)

    print("First 5 months preview:")
    print(df.head())

    save_to_csv(df)
    plot_chart(df)


if __name__ == "__main__":
    main()