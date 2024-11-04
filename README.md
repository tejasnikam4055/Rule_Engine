

# Rule Engine Dashboard

A web-based rule engine dashboard that allows users to create, evaluate, and manage business rules using a simple interface. The system uses a Python backend with Flask and MySQL for storage, featuring a modern, responsive frontend.

## Features

- **Create and Store Business Rules**: Users can define custom conditions and save them for future evaluations.
- **Evaluate Data Against Stored Rules**: Easily check if the given data satisfies specific business rules.
- **Delete Existing Rules**: Remove rules that are no longer needed to keep the rule set clean.
- **Interactive Web Interface**: User-friendly design for efficient rule management and evaluation.
- **Support for Complex Logical Operations**: Use logical operations like AND and OR to create sophisticated rules.
- **Persistent Storage**: All rules are stored in a MySQL database for durability and retrieval.

## Prerequisites

Before you begin, ensure you have the following installed:
- **Python 3.7+**
- **MySQL Server**
- **pip** (Python package manager)

## Installation

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd rule-engine-dashboard
    ```

2. **Create a virtual environment and activate it**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use: venv\Scripts\activate
    ```

3. **Install required dependencies**:
    ```bash
    pip install flask mysql-connector-python
    ```

4. **Set up the MySQL database**:
    ```sql
    CREATE DATABASE rule_engine;
    ```

5. **Configure the database connection**:
   Update the following values in `app.py` according to your MySQL setup:
    ```python
    host='localhost'
    user='root'
    password='your_password'
    database='rule_engine'
    ```

## Project Structure

```
rule-engine/
├── app.py              # Flask application
├── ast9.py             # Rule parsing and evaluation logic
├── db.py               # Database operations
├── templates/
│   └── index2.html     # Frontend template
├── static/
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript files
└── README.md
```

## Usage

1. **Start the Flask application**:
    ```bash
    python app.py
    ```

2. **Open your web browser and navigate to**:
    ```
    http://localhost:5000
    ```

3. **Use the dashboard to**:
   - Add new rules using the rule syntax.
   - Evaluate data against existing rules.
   - Delete rules when no longer needed.

### Rule Syntax

Rules should be written using the following syntax:
- **Simple condition**: `field operator value`
- **Complex condition**: `condition1 AND/OR condition2`

**Examples**:
```
age > 18
income >= 50000
age > 18 AND income >= 50000
(age > 18 AND income >= 50000) OR status = "premium"
```

**Supported Operators**:
- `>` (greater than)
- `>=` (greater than or equal)
- `<` (less than)
- `<=` (less than or equal)
- `=` (equal)
- `!=` (not equal)

### Data Format

When evaluating rules, provide data in JSON format:
```json
{
    "age": 25,
    "income": 60000,
    "status": "premium"
}
```

### API Endpoints

#### Rules

- **`GET /rules`**: Retrieve all rules.
- **`POST /rules`**: Create a new rule.
- **`DELETE /rules/<id>`**: Delete a specific rule.

#### Evaluation

- **`POST /evaluate`**: Evaluate data against a rule.
- **`GET /evaluate`**: Retrieve evaluation results.

## Frontend Components

The dashboard includes three main sections:

1. **Add Rule Card**:
   - Input field for rule creation.
   - Add button to submit the rule.

2. **Evaluate Rule Card**:
   - Input fields for rule ID and data.
   - Evaluate button to check the rule.

3. **Delete Rule Card**:
   - Input field for rule ID.
   - Delete button to remove the rule.

## Error Handling

The application includes comprehensive error handling for:
- Invalid rule syntax.
- Missing or malformed data.
- Database connection issues.
- Invalid JSON format.
- Missing required fields.

## Testing

### Automated Tests

To ensure reliability, consider adding unit tests. You can use Python's built-in `unittest` framework. Create a separate `tests/` directory and write test cases for your functions.

1. **Run tests**:
    ```bash
    python -m unittest discover tests
    ```

### Manual Testing

Test the application by manually creating, evaluating, and deleting rules. Verify that the expected results are returned for various inputs.

## Deployment

For deployment, consider using services like Heroku, AWS, or DigitalOcean. Ensure that environment variables for database connections and secrets are properly managed.

## Contributing

1. **Fork the repository**.
2. **Create your feature branch**:
    ```bash
    git checkout -b feature/AmazingFeature
    ```
3. **Commit your changes**:
    ```bash
    git commit -m 'Add some AmazingFeature'
    ```
4. **Push to the branch**:
    ```bash
    git push origin feature/AmazingFeature
    ```
5. **Open a Pull Request**.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

