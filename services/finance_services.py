def calculate_compound_interest(principal: float, rate: float, time: float, n: int):
    # A = P(1 + r/n)^(nt)
    amount = principal * (1 + rate / (n * 100)) ** (n * time)
    return round(amount, 2)
# services/finance_services.py

def calculate_simple_interest(principal: float, rate: float, time: float) -> float:
    return principal * rate * time
