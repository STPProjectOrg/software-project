from django.test import SimpleTestCase
from dashboard_app.forms import TransactionAddForm, TransactionUpdateForm

class TestForms(SimpleTestCase):

    #TransactionAddForm
    def test_add_to_portfolio_form_valid_data(self):
        form = TransactionAddForm(data={
            'sell':False,
            'amount':10,
            'date': "2022-2-2",
            'price': 250000,
            'tax': 20,
            'charge': 10,
            'post' : True,
            'postText': "Test-test",
            'tags': "test-Tag"

        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.data["sell"], False)
        self.assertEqual(form.data["amount"], 10)
        self.assertEqual(form.data["date"], "2022-2-2")
        self.assertEqual(form.data["price"], 250000)
        self.assertEqual(form.data["tax"], 20)
        self.assertEqual(form.data["charge"], 10)
        self.assertEqual(form.data["post"], True)
        self.assertEqual(form.data["postText"], "Test-test")
        self.assertEqual(form.data["tags"], "test-Tag")


    def test_add_to_portfolio_form_no_data(self):
        form = TransactionAddForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)

    #TransactionAddForm
    def test_transaction_update_form_valid_data(self):
        form = TransactionUpdateForm(data={
            'amount':1,
            'date': "2022-2-3",
            'price': 25000,
            'tax': 5,
            'charge': 1,
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.data["amount"], 1)
        self.assertEqual(form.data["date"], "2022-2-3")
        self.assertEqual(form.data["price"], 25000)
        self.assertEqual(form.data["tax"], 5)
        self.assertEqual(form.data["charge"], 1)


    def test_transaction_update_form_no_data(self):
        form = TransactionUpdateForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)


    


