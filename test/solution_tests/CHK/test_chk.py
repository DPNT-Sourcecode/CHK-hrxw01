from solutions.CHK import checkout_solution


class TestCheckout:
    def test_chk(self):
        skus = "ABC"
        assert checkout_solution.checkout(skus) == 100

    def test_deal_a(self):
        skus = "AAA"
        assert checkout_solution.checkout(skus) == 130

    def test_invalid_sku(self):
        skus = "ABCDE"
        assert checkout_solution.checkout(skus) == -1

    def test_bad_case(self):
        skus = "aaBBB"
        assert checkout_solution.checkout(skus) == 175
