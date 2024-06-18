from solutions.CHK import checkout_solution


class TestCheckout:
    def test_chk(self):
        skus = "ABC"
        assert checkout_solution.checkout(skus) == 100

    def test_deal_a(self):
        skus = "AAA"
        assert checkout_solution.checkout(skus) == 130

    def test_deal_a_2(self):
        skus = "A" * 6
        assert checkout_solution.checkout(skus) == 250

    def test_deal_a_3(self):
        skus = "A" * 8
        assert checkout_solution.checkout(skus) == 330

    def test_deal_a_4(self):
        skus = "A" * 8 + "B" * 2
        print(skus)
        assert checkout_solution.checkout(skus) == 375

    def test_free_b_for_2e(self):
        skus = "EEB"
        assert checkout_solution.checkout(skus) == 80

    def test_invalid_sku(self):
        skus = "ABCDE"
        assert checkout_solution.checkout(skus) == -1

    def test_bad_case(self):
        skus = "aaBBB"
        assert checkout_solution.checkout(skus) == -1

    def test_empty(self):
        skus = ""
        assert checkout_solution.checkout(skus) == 0


