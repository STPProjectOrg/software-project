from django.test import SimpleTestCase
from dashboard_app.forms import AddToPortfolioForm, AddToPortfolioForm2, TransactionBuyForm

class TestForms(SimpleTestCase):

    #AddToPortfolio Form
    def test_add_to_portfolio_form_valid_data(self):
        form = AddToPortfolioForm(data={
            'user': 'TestUser',
            'assetDropdown': "TestCoins",
            'amount': 200,
            'purchaseDate': "2022-2-2"
        })

        self.assertTrue(form.is_valid())


    def test_add_to_portfolio_form_no_data(self):
        form = AddToPortfolioForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    # AddToPortfolio2 Form
    def test_add_to_portfolio2_form_valid_data(self):
        form = AddToPortfolioForm2(data={
            'user': 'TestUser',
            'assetDropdown': "TestCoins",
            'amount': 200,
            'purchaseDate': "2022-2-2"
        })

        self.assertTrue(form.is_valid())


    def test_add_to_portfolio2_form_no_data(self):
        form = AddToPortfolioForm2(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)
    
    # TransactionBuy Form
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


    def test_transaction_buy_form_no_data(self):
        form = TransactionBuyForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)