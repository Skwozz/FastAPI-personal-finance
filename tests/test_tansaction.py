# import pytest
#
#
# @pytest.mark.asyncio
# async def test_create_transaction(authorized_client):
#     category_data = {
#         'name': 'Еда',
#         'type': 'EXPENSE'
#     }
#     response = await authorized_client.post('/categories/',json=category_data)
#     assert response.status_code == 200
#     category_id = response.json()['id']
#
#     transaction_data = {
#         'amount':'1000',
#         'description': 'Овощи',
#         'date': '2025-04-30',
#         'category_id': category_id
#     }
#
#     response = await authorized_client.post('/transactions/',json=transaction_data)
#     assert response.status_code == 200
#     transaction = response.json()
#     assert transaction["amount"] == 1000
#     assert transaction["description"] == "Овощи"
#     assert transaction["category_id"] == category_id