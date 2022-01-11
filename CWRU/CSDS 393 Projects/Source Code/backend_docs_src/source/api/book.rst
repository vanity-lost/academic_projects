/book/
=======================

This is the page for all accounting book related APIs

/book/create - ``POST``
----------------------------------------
Create a new accounting book.

.. NOTE::

    Here, ``members`` is optional. We can discuss this later and change it.

**Full Request Path**
``POST`` - ``/book/create``

**Sample Request Param**

.. code-block:: json

    {
        "name": "Test Book"
    }

**Sample Response**

.. code-block:: json

    {
        "code": "SUCCESS",
        "message": "",
        "data": {
            "id": 17,
            "name": "Test Book2",
            "owner": "codetectorwww",
            "members": [
                "violetaab"
            ]
        }
    }

/book/list - ``GET``
----------------------------------------
List all accounting books which belong to that account.


**Full Request Path**
``GET`` - ``/book/list``

**Sample Response**

.. code-block:: json

    {
        "code": "SUCCESS",
        "message": "",
        "data": [
            {
                "id": 14,
                "name": "Test Book1",
                "owner": "codetectorwww",
                "members": []
            },
            {
                "id": 17,
                "name": "Test Book2",
                "owner": "codetectorwww",
                "members": [
                    "violetaab"
                ]
            }
        ]
    }

/book/member - ``POST``
----------------------------------------
Set the list of members for an accounting book.

.. NOTE::

    Here, you need to parse all the members.

**Full Request Path**
``POST`` - ``/book/member``

**Sample Request Param**

.. code-block:: json

    {
        "bookId": 14,
        "members": ["violetaab"]
    }

**Sample Response**

.. code-block:: json

    {
        "code": "SUCCESS",
        "message": "",
        "data": {
            "id": 14,
            "name": "Test Book1",
            "owner": "codetectorwww",
            "members": [
                "violetaab"
            ]
        }
    }

/book/category/add - ``POST``
----------------------------------------
Add a new category to an accounting book.

**Full Request Path**
``POST`` - ``/book/category/add``

**Sample Request Param**

.. code-block:: json

    {
        "name": "aaaaa",
        "accountingBookId": 14
    }

**Sample Response**

.. code-block:: json

    {
        "code": "SUCCESS",
        "message": "",
        "data": {
            "id": 19,
            "name": "aaaaa"
        }
    }

/book/category/edit - ``POST``
----------------------------------------
Change category name.


**Full Request Path**
``POST`` - ``/book/category/edit``

**Sample Request Param**

.. code-block:: json

    {
        "name": "food",
        "categoryId": 19
    }

**Sample Response**

.. code-block:: json

    {
        "code": "SUCCESS",
        "message": "",
        "data": {
            "id": 19,
            "name": "food"
        }
    }

/book/category/delete - ``DELETE``
----------------------------------------
Delete a category.


**Full Request Path**
``DELETE`` - ``/book/category/delete``

**Sample Request Param**

.. code-block:: json

    {
        "categoryId": 20
    }

**Sample Response**

.. code-block:: json

    {
        "code": "SUCCESS",
        "message": "",
        "data": null
    }

/book/category/list - ``POST``
----------------------------------------
Get all categories of an accounting book.


**Full Request Path**
``POST`` - ``/book/category/list``

**Sample Request Param**

.. code-block:: json

    {
        "accountingBookId": 14
    }

**Sample Response**

.. code-block:: json

    {
        "code": "SUCCESS",
        "message": "",
        "data": [
            {
                "id": 18,
                "name": "aaaaa"
            },
            {
                "id": 19,
                "name": "food"
            }
        ]
    }

/book/entry/add - ``POST``
----------------------------------------
Add an entry for an accounting book.


**Full Request Path**
``POST`` - ``/book/entry/add``

**Sample Request Param**

.. code-block:: json

    {
        "amount": 25,
        "description": "ttt",
        "date": 1604522957,
        "categoryId": 19,
        "author": "violetaab",
        "participants": ["violetaab", "codetectorwww"],
        "accountingBookId": 14
    }

**Sample Response**

.. code-block:: json

    {
        "code": "SUCCESS",
        "message": "",
        "data": {
            "id": 21,
            "amount": 25.0,
            "description": "ttt",
            "date": 1604522957,
            "category": {
                "id": 19,
                "name": "food"
            },
            "author": {
                "username": "violetaab",
                "nickname": "vio",
                "email": "viola@gmail.com",
                "phone": "123-456-7890"
            },
            "participants": [
                {
                    "username": "violetaab",
                    "nickname": "vio",
                    "email": "viola@gmail.com",
                    "phone": "123-456-7890"
                },
                {
                    "username": "codetectorwww",
                    "nickname": "codetector",
                    "email": "codetector@gmail.com",
                    "phone": "123-456-7833"
                }
            ],
            "accountingBook": {
                "id": 14,
                "name": "Test Book1",
                "owner": "codetectorwww",
                "members": [
                    "violetaab"
                ]
            }
        }
    }

/book/entry/edit - ``POST``
----------------------------------------
Edit an entry.

.. NOTE::

    Here, you need to parse all the informations for an entry.

**Full Request Path**
``POST`` - ``/book/entry/edit``

**Sample Request Param**

.. code-block:: json

    {
        "entryId": 21,
        "amount": 10,
        "description": "Fffffood",
        "date": 1604522957,
        "categoryId": 19,
        "author": "violetaab",
        "participants": ["violetaab"],
        "accountingBookId": 14
    }

**Sample Response**

.. code-block:: json

    {
        "code": "SUCCESS",
        "message": "",
        "data": {
            "id": 21,
            "amount": 10.0,
            "description": "Fffffood",
            "date": 1604522957,
            "category": {
                "id": 19,
                "name": "food"
            },
            "author": {
                "username": "violetaab",
                "nickname": "vio",
                "email": "viola@gmail.com",
                "phone": "123-456-7890"
            },
            "participants": [
                "violetaab"
            ],
            "accountingBook": {
                "id": 14,
                "name": "Test Book1",
                "owner": "codetectorwww",
                "members": [
                    "violetaab"
                ]
            }
        }
    }

/book/entry/delete - ``DELETE``
----------------------------------------
Delete an entry.

**Full Request Path**
``DELETE`` - ``/book/entry/delete``

**Sample Request Param**

.. code-block:: json

    {
        "entryId": 23
    }

**Sample Response**

.. code-block:: json

    {
        "code": "SUCCESS",
        "message": "",
        "data": null
    }

/book/entry/list - ``POST``
----------------------------------------
Get all entries for an accounting book.


**Full Request Path**
``POST`` - ``/book/entry/add``

**Sample Request Param**

.. code-block:: json

    {
        "accountingBookId": 14
    }

**Sample Response**

.. code-block:: json

    {
        "code": "SUCCESS",
        "message": "",
        "data": [
            {
                "id": 21,
                "amount": 10.0,
                "description": "Fffffood",
                "date": 1604522957,
                "category": {
                    "id": 19,
                    "name": "food"
                },
                "author": {
                    "username": "violetaab",
                    "nickname": "vio",
                    "email": "viola@gmail.com",
                    "phone": "123-456-7890"
                },
                "participants": [
                    "violetaab"
                ],
                "accountingBook": {
                    "id": 14,
                    "name": "Test Book1",
                    "owner": "codetectorwww",
                    "members": [
                        "violetaab"
                    ]
                }
            },
            {
                "id": 22,
                "amount": 300.0,
                "description": "ttt",
                "date": 1604522957,
                "category": {
                    "id": 19,
                    "name": "food"
                },
                "author": "violetaab",
                "participants": [
                    "violetaab",
                    {
                        "username": "codetectorwww",
                        "nickname": "codetector",
                        "email": "codetector@gmail.com",
                        "phone": "123-456-7833"
                    }
                ],
                "accountingBook": {
                    "id": 14,
                    "name": "Test Book1",
                    "owner": "codetectorwww",
                    "members": [
                        "violetaab"
                    ]
                }
            }
        ]
    }

/book/split - ``POST``
----------------------------------------
Get the splitted amount for a user of an accounting book.

.. NOTE::

    Only the members of the accounting book could see the splitted results. Member A could see member B's amount.

**Full Request Path**
``POST`` - ``/book/split``

**Sample Request Param**

.. code-block:: json

    {
        "accountingBookId": 14,
        "username": "codetectorwww"
    }

**Sample Response**

.. code-block:: json

    {
        "code": "SUCCESS",
        "message": "",
        "data": {
            "codetectorwww": 150.0
        }
    }