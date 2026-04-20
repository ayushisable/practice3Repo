import datetime

class OrderProcessor:

    def __init__(self):
        self.orders = []

    def parse_orders(self, raw_data):
        parsed_orders = []

        for item in raw_data:
            order = {}

            # BUG 1: KeyError if 'id' missing
            order["id"] = int(item["id"])

            # BUG 2: Wrong key name (should be 'amount')
            try:
                order["amount"] = float(item.get("amount"))
            except:
                order["amount"] = 0.0

            try:
                order["date"] = datetime.datetime.strptime(item["date"], "%Y-%m-%d")
            except:
                try:
                    order["date"] = datetime.datetime.strptime(item["date"], "%d-%m-%Y")
                except:
                    print("Invalid date:", item["date"])
                    order["date"] = None


            parsed_orders.append(order)

        return parsed_orders

    def calculate_total(self, orders):
        total = 0

        for order in orders:
            # BUG 4: NoneType error possible
            total += order["amount"]

        return total

    def find_large_orders(self, orders, threshold):
        large_orders = []

        for order in orders:
            # BUG 5: Logic error (should be > but used <)
            if order["amount"] < threshold:
                large_orders.append(order)

        return large_orders


# Sample Data (contains issues)
data = [
    {"id": "1", "amount": "100", "date": "2024-01-10"},
    {"id": "2", "amt": "200", "date": "2024-02-15"},   # wrong key
    {"id": "3", "amount": None, "date": "2024-03-20"}, # None issue
    {"id": "4", "amount": "400", "date": "20-04-2024"} # wrong date format
]

processor = OrderProcessor()

parsed = processor.parse_orders(data)
total = processor.calculate_total(parsed)
large = processor.find_large_orders(parsed, 150)

print("Total:", total)
print("Large Orders:", large)