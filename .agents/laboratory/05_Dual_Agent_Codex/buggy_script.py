def calculate_discount(price, discount_percent):
    """
    Calculates the final price after applying a discount percentage.
    """
    # [BUG] Intentional logic bug: It subtracts the percentage directly as a flat value.
    # Expected: price - (price * (discount_percent / 100))
    final_price = price - discount_percent
    return final_price

if __name__ == "__main__":
    # Test case: 200원짜리 물건을 20% 할인하면 160원이 나와야 하는데,
    # 현 로직은 200 - 20 = 180원이 나옴.
    val = calculate_discount(200, 20)
    print(f"Price after 20% discount on 200: {val}")
