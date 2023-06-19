from django.test import SimpleTestCase
from dashboard_app.forms import AddToPortfolioForm, AddToPortfolioForm2, TransactionBuyForm

class TestForms(SimpleTestCase):

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
