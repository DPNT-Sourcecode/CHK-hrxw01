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
        skus = "ABCD123"
        assert checkout_solution.checkout(skus) == -1

    def test_bad_case(self):
        skus = "aaBBB"
        assert checkout_solution.checkout(skus) == -1

    def test_empty(self):
        skus = ""
        assert checkout_solution.checkout(skus) == 0

    def test_2f_get_free_f(self):
        assert checkout_solution.checkout("F" * 2) == 20
        assert checkout_solution.checkout("F" * 4) == 30
        assert checkout_solution.checkout("F" * 6) == 40

    def test_3u_get_free_u(self):
        assert checkout_solution.checkout("U" * 3) == 120
        assert checkout_solution.checkout("U" * 4) == 120
        assert checkout_solution.checkout("U" * 5) == 160

    def test_3n_get_free_m(self):
        assert checkout_solution.checkout("NNNM") == 120
        assert checkout_solution.checkout("NNN") == 120

    def test_group_discount(self):
        assert checkout_solution.checkout("STX") == 45
        assert checkout_solution.checkout("STXZ") == 65
        assert checkout_solution.checkout("STXZYZ") == 85
