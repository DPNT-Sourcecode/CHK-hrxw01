from solutions.CHK import checkout_solution


class TestCheckout:
    def test_chk(self):
        skus = "A,B,C"
        assert checkout_solution.checkout(skus) == 100

    def test_deal_a(self):
        skus = "A,A,A"
        assert checkout_solution.checkout(skus) == 130

    def test_invalid_sku(self):
        skus = "A,B,C,D,E"
        assert checkout_solution.checkout(skus) == -1

