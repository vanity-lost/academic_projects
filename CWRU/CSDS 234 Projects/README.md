# Amazon co-purchasing analysis

## Three tables

1. products
   - attributes: ASIN, title, group, salesrank, co_purchased_num, categories, reviews_num, avg_rate, first_time, last_time, highest_rate, lowest_rate
2. customers
   - attributes: id, product, time, rating, votes, helpful
3. co_purchased
   - attributes: first, second

## Query Engine

- Python Pandas Dataframe

## Prediction Model

- Logistic Regression
- 92.7% accuracy

## Recommendation System

_model is used to provide co-purchasing link strength_

- Three functionalities:

  - Given a customer, find which product the customer will be interested in
  - Given a product, find which customer will be interested in
  - Givne a new product, find which customer will be interested in
