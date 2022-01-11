/auth/
=======================

This is the page for all authentication / authorization related APIs

/auth/register - ``POST``
----------------------------------------
Register a new account.

.. NOTE::

    Here, ``nickname`` and ``phone`` are optional. We can discuss this later and change it.

**Full Request Path**
``POST`` - ``/auth/register``

**Sample Request Param**

.. code-block:: json

    {
        "username": "alice",
        "password": "totallysecure",
        "nickname": "Alice the Cutie",
        "phone": "888-888-8888",
        "email": "abc@abc.com"
    }

**Sample Response**

.. code-block:: json

    {
    "code": "SUCCESS",
    "time": 9999999,
    "message": "",
    "data":
        {
            "id": 7,
            "nickname": "Alice the Cutie",
            "username": "alice",
            "email": "abc@abc.com",
            "phone": "888-888-8888"
        }
    }

/auth/auth - ``POST``
----------------------------------------
Login to an account

.. NOTE::

    Here, ``username`` can be any of ``email``, ``username``, or ``phone`` we can discuss this and change it etc.
    Please make sure you save the "token" returned. Set this to the header "Authorization"'s value to show that you
    are authenticated.

**Full Request Path**
``POST`` - ``/auth/auth``

**Sample Request Param**

.. code-block:: json

    {
        "username": "alice",
        "password": "totallysecure"
    }

**Sample Response**

.. code-block:: json

    {
        "code": "SUCCESS",
        "message": "",
        "data": {
            "token": "35f7c76f-f1d8-439b-bb47-3f9fcfe5e048",
            "account": {
                "nickname": "Alice the Cutie",
                "username": "alice",
                "email": "abc@abc.com",
                "phone": "888-888-8888"
            },
            "lastActive": 1603516433,
            "created": 1603516433
        }
    }

/auth/me - ``GET``
----------------------------------------
Show who's logged in. This is here so you can test your header works



**Full Request Path**
``POST`` - ``/auth/auth``

**Sample Request Param**

Header: "Authorization": ``token you got from /auth/auth``


**Sample Response**

.. NOTE::
    This should be identical to the /auth/auth response. You will get HTTP 403 if not logged in.

.. code-block:: json

    {
        "code": "SUCCESS",
        "message": "",
        "data": {
            "token": "35f7c76f-f1d8-439b-bb47-3f9fcfe5e048",
            "account": {
                "nickname": "Alice the Cutie",
                "username": "alice",
                "email": "abc@abc.com",
                "phone": "888-888-8888"
            },
            "lastActive": 1603516433,
            "created": 1603516433
        }
    }

/auth/reset - ``POST``
----------------------------------------
Request a password reset and perform the reset. Depending on how the reuqest is
formed.


**Full Request Path**
``POST`` - ``/auth/auth``

**Sample Request Param**

.. NOTE::
    if ``code`` is empty, then password is not used (can be empty). It will request a password reset
    code to the specified account. If code is present, then password must also be present. If the code
    supplied is correct, then a password reset operation will be performed. Also a side effect of this
    is that all currently logged in session associated with this account will be KICKED OUT.

.. code-block:: json

    {
        "username": "codetector",
        "password": "lollollol",
        "code": "10359540"
    }

**Sample Response**


For a code request:

.. code-block:: json

    {
        "code": "SUCCESS",
        "message": "",
        "data": "Email Sent"
    }

For a reset:

.. code-block:: json

    {
        "code": "SUCCESS",
        "message": "",
        "data": "Success"
    }


/auth/test_delete - ``DELETE``
----------------------------------------
Delete a user **TESTING ONLY**


**Full Request Path**
``DELETE`` - ``/auth/test_delete``

.. NOTE::
    Testing only api. Will delete the selected user.


**Sample Request Param**


.. code-block:: json

    {
        "username": "thing"
    }
