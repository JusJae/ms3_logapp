### Access the Python Interpreter

- `python3`

### Import the 'mongo' instance from app.py

- `from app import mongo`

### Create Index on the 'products' collection, using 'product_name', 'product_notes' and 'product_category' keys

- **NOTE**: You can only have a maximum of ONE Index on the collection, but multiple keys permitted on that Index.
  
- `mongo.db.tasks.create_index([("product_name", "text"), ("product_notes", "text"), ("product_category", "text")])`

### See all Index information

- `mongo.db.products.index_information()`

### Drop/Delete a single Index

- `mongo.db.products.drop_index('product_name_text_product_notes_text_product_category_text')`

### Drop/Delete all Indexes

- `mongo.db.products.drop_indexes()`

### Quit the Python Interpreter

- `quit()`
