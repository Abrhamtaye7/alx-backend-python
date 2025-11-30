import sys
from bank_account import BankAccount
from robust_division_calculator import safe_divide

def main():
    # Create a bank account with an initial balance of $100
    account = BankAccount(100)

    # Ensure the user provided at least one command
    if len(sys.argv) < 2:
        print("Usage: python main-0.py <command>:<amount>")
        print("Commands: deposit, withdraw, display")
        sys.exit(1)

    # Parse the command entered by the user
    command, *params = sys.argv[1].split(':')

    # Extract amount if provided
    amount = float(params[0]) if params else None

    # Handle deposit command
    if command == "deposit" and amount is not None:
        account.deposit(amount)
        print(f"Deposited: ${amount}")

    # Handle withdraw command
    elif command == "withdraw" and amount is not None:
        if account.withdraw(amount):
            print(f"Withdrew: ${amount}")
        else:
            print("Insufficient funds.")

    # Handle displaying the balance
    elif command == "display":
        account.display_balance()

    # Handle any invalid commands
    else:
        print("Invalid command.")

if __name__ == "__main__":
    main()
