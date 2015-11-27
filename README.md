##TodoList API

`create_user/`
`POST` here with `username, password` and optionally `email` fields to create a
user which you can then use to authenticate requests to other endpoints.

`lists/`
Main endpoint for TodoList items. Requires authentication.
`GET` returns all lists created by your user.
`POST` with `name` field to create a new list, or `PUT/PATCH` at `lists/<id>` to update that list.
`DELETE` at `lists/<id>` will delete the list.

`items/`
Main endpoint for TodoItem items. Requires authentication.
`GET` returns all items created by your user.
`POST` with `name, list` fields to create a new item, or `PUT/PATCH` at `items/<id>` to update that item.
`DELETE` at `lists/<id>` will 'delete' the item.

`recover/<id>`
`POST` here to restore an item created and deleted by your user.

`users/`
`GET` returns a list of users.