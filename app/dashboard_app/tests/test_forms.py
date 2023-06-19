from django.test import SimpleTestCase
from dashboard_app.forms import AddToPortfolioForm, AddToPortfolioForm2, TransactionBuyForm

class TestForms(SimpleTestCase):

    #AddToPortfolioForm
    def test_add_to_portfolio_form_valid_data(self):
        form = AddToPortfolioForm(data={
            'user': 'TestUser',
            'assetDropdown': "TestCoins",
            'amount': 200,
            'purchaseDate': "2022-2-2"
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.data["user"], "TestUser")
        self.assertEqual(form.data["assetDropdown"], "TestCoins")
        self.assertEqual(form.data["amount"], 200)
        self.assertEqual(form.data["purchaseDate"], "2022-2-2")


    def test_add_to_portfolio_form_no_data(self):
        form = AddToPortfolioForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    # AddToPortfolio2Form
    def test_add_to_portfolio2_form_valid_data(self):
        form = AddToPortfolioForm2(data={
            'user': 'TestUser',
            'assetDropdown': "TestCoins",
            'amount': 200,
            'purchaseDate': "2022-2-2"
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.data["user"], "TestUser")
        self.assertEqual(form.data["assetDropdown"], "TestCoins")
        self.assertEqual(form.data["amount"], 200)
        self.assertEqual(form.data["purchaseDate"], "2022-2-2")


    def test_add_to_portfolio2_form_no_data(self):
        form = AddToPortfolioForm2(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)
    
    # TransactionBuyForm
    def test_transaction_buy_form_valid_data(self):
        form = TransactionBuyForm(data={
            'amount': 200,
            'date':  "2022-2-2",
            'price': 2,
            'tax': 1.05,
            'charge': 1.1,
            'post': False,
            'postText': 'Test',
            'tags': 'Test Tags'
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.data["amount"], 200)
        self.assertEqual(form.data["date"], "2022-2-2")
        self.assertEqual(form.data["price"], 2)
        self.assertEqual(form.data["tax"], 1.05)
        self.assertEqual(form.data["charge"], 1.1)
        self.assertEqual(form.data["post"], False)
        self.assertEqual(form.data["postText"], "Test")
        self.assertEqual(form.data["tags"], "Test Tags")


    def test_transaction_buy_form_no_data(self):
        form = TransactionBuyForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)