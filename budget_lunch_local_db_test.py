import unittest
import budget_lunch_local_db


class TestBudgetLunchLocalDB(unittest.TestCase):

    lunch_db = [
        {
            "name" : "pizza",
            "price" : 6.99,
            "imageurl" : "https://ooni.com/cdn/shop/articles/20220211142347-margherita-9920_ba86be55-674e-4f35-8094-2067ab41a671.jpg?v=1737104576&width=1080"
        },
        {
            "name" : "salad",
            "price" : 5.99,
            "imageurl" : "https://cdn.loveandlemons.com/wp-content/uploads/2021/04/green-salad.jpg"
        },
        {
            "name" : "soda",
            "price" : 1.99,
            "imageurl" : "https://i5.walmartimages.com/asr/bba96e0f-0444-4b2b-8e55-d90edf928e00.cf87606a804ac13e7807cd48dbd53792.jpeg"
        },    
        {
            "name" : "coffee",
            "price" : 2.99,
            "imageurl" : "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQO9TfIFqT5Np6d9CSiJB0QdXnOGE2NPaOXGQ&s"
        }
    ]


    def test_search_food_with_price(self):
        self.assertEqual(budget_lunch_local_db.search_food_with_price(10), self.lunch_db)

    def test_search_food_with_price_2(self):
        self.assertEqual(budget_lunch_local_db.search_food_with_price(2), [self.lunch_db[2]])

if __name__ == "__main__":
    unittest.main()