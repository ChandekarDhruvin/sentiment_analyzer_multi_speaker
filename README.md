
# Employee Dashboard

This is a Streamlit-based Employee Dashboard designed to allow employees, managers, and HR to access various data points, including skill recommendations, task recommendations, sentiment analysis, and meeting information. It uses a PostgreSQL database to store and manage employee-related data and provides role-based dashboards for users.

## Features

- **Login**: Secure login for employees based on their email.
- **Employee Dashboard**: Displays meeting data, skill and task recommendations, and sentiment analysis.
- **Manager Dashboard**: Provides access to personal data and allows viewing data for team members.
- **HR Dashboard**: Displays individual employee data and gives an overview of the entire organization's structure and statistics.
- **Sentiment Analysis**: Displays sentiment scores for meetings and shows rolling sentiment charts.
- **Data Storage**: PostgreSQL database is used for storing employee, skills, tasks, and sentiment data.

## Requirements

- Python 3.x
- Streamlit
- SQLAlchemy
- pandas
- psycopg2
- dotenv

## Setup

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/employee-dashboard.git
   cd employee-dashboard
   ```

2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your PostgreSQL database URL:
   ```bash
   DATABASE_URL=your_database_url_here
   ```

4. Run the app:
   ```bash
   streamlit run app.py
   ```

## File Structure

- **app.py**: The main Streamlit application file.
- **models.py**: Contains SQLAlchemy ORM models for the database.
- **.env**: Environment file to store sensitive information like database URL.
- **requirements.txt**: Lists the dependencies for the project.

## Screenshots

![Screenshot 2025-04-21 114632](https://github.com/user-attachments/assets/ec9019a9-5ba6-4c77-b4e7-f5be15faed94)
