import os
import logging
import sys
import time
from sqlalchemy import create_engine, MetaData, Table, select, func
import ollama
import requests

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Set Ollama base URL to connect to the host machine
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://host.docker.internal:11434')
logger.info(f"Ollama Base URL: {OLLAMA_BASE_URL}")

# Set up database connection
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://admin:XXXXXX@db/exampledb')
engine = create_engine(DATABASE_URL)
metadata = MetaData()
metadata.reflect(bind=engine)
alert_table = Table('alert', metadata, autoload_with=engine)


# Function to interact with the local LLM (Ollama/llama3)
def query_llm(query):
    try:
        response = ollama.chat(model='llama3', messages=[
            {
                'role': 'user',
                'content': 'What is alert in prometheus and alertmanager?',
            },
        ])
        response.raise_for_status()
        data = response.json()
        return data['message']['content']
    except Exception as e:
        logger.error(f"Error querying LLM: {e}")
        return f"Error: Unable to process query with LLM"
# def query_llm(query):
#     try:
#         logger.debug(f"Sending query to LLM: {query}")
#         start_time = time.time()
#         response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json={
#             "model": "llama3",
#             "prompt": query
#         }, timeout=30)  # 30 seconds timeout
#         end_time = time.time()
#         logger.debug(f"LLM response time: {end_time - start_time:.2f} seconds")
#
#         if response.status_code == 200:
#             return response.json().get('response', "No response content")
#         else:
#             logger.error(f"LLM request failed with status code: {response.status_code}")
#             return f"Error: LLM request failed with status code {response.status_code}"
#     except requests.exceptions.Timeout:
#         logger.error("LLM request timed out")
#         return "Error: LLM request timed out"
#     except requests.exceptions.RequestException as e:
#         logger.error(f"Error querying LLM: {e}")
#         return f"Error: Unable to process query with LLM - {str(e)}"


# Query function
def query_database(query):
    with engine.connect() as connection:
        result = connection.execute(query)
        return result.fetchall()


# Handle natural language query with RAG
def handle_query(natural_language_query):
    # Step 1: Use the LLM to process the natural language query
    # llm_response = query_llm(natural_language_query)
    # logger.info(f"LLM Response: {llm_response}")

    # Step 2: Determine if the query should interact with the PostgreSQL database
    if "alert" in natural_language_query.lower():
        if "earliest start_time" in natural_language_query.lower():
            sql_query = select(alert_table).order_by(alert_table.c.start_time.asc()).limit(1)
        else:
            sql_query = select(alert_table)
        results = query_database(sql_query)
        logger.info(f"Database Results: {results}")

        # Combine the LLM response with the PostgreSQL data
        combined_response = {
            "llm_response": "llm_response",
            "database_results": results
        }
        #
        return combined_response
    else:
        return "llm_response"


# LangChain integration
class DatabaseLangChain:
    def process_query(self, user_query):
        response = handle_query(user_query)
        return response


# Main function for interactive testing
def main():
    langchain_app = DatabaseLangChain()
    print("Welcome to the LangChain PostgreSQL QA System!")
    print("Enter your questions or type 'exit' to quit.")

    while True:
        try:
            user_query = input("\nEnter your question: ")
            if user_query.lower() == 'exit':
                print("Thank you for using the QA system. Goodbye!")
                break

            logger.info(f"Received user query: {user_query}")
            response = langchain_app.process_query(user_query)
            print("\nResponse:")
            print(response)
        except EOFError:
            print("Input stream closed. Exiting.")
            break
        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            logger.exception("An unexpected error occurred")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("An unexpected error occurred in the main function")
        sys.exit(1)