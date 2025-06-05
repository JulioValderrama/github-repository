import requests
import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv

# === 1. Cargar variables del entorno ===
load_dotenv(dotenv_path="/opt/n8n/.env")  # Busca .env en el mismo directorio

# === 2. Configuración vía entorno ===
AGENT_WEBHOOK_URL = os.environ["AGENT_WEBHOOK_URL"]
WEBHOOK_HEADER = {
    os.environ["AGENT_SECRET_HEADER_NAME"]: os.environ["AGENT_SECRET_HEADER_VALUE"]
}
DB_HOST = os.environ["TEST_DB_HOST"]
DB_PORT = int(os.environ["TEST_DB_PORT"])
DB_NAME = os.environ["TEST_DB_DATABASE"]
DB_USER = os.environ["TEST_DB_USER"]
DB_PASSWORD = os.environ["TEST_DB_PASSWORD"]

# === 3. Conexión a la base de datos ===
def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# === 4. Leer preguntas y respuestas esperadas ===
def fetch_questions():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, question_text, expected_answer FROM questions_base ORDER BY id ASC;")
            return cur.fetchall()

# === 5. Guardar resultado del test ===
def save_result(question_id, agent_answer):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO agent_test_results (question_id, agent_answer, tested_at) VALUES (%s, %s, %s)",
                (question_id, agent_answer, datetime.now())
            )
            conn.commit()

# === 6. Probar agente: enviar pregunta y guardar respuesta ===
def main():
    questions = fetch_questions()
    print(f"⏳ Lanzando {len(questions)} preguntas al agente...\n")

    for qid, qtext, expected in questions:
        data = {"question": qtext}
        try:
            resp = requests.post(AGENT_WEBHOOK_URL, headers=WEBHOOK_HEADER, json=data, timeout=30)
            # Si la respuesta es JSON con campo 'answer', toma eso. Si no, guarda el texto tal cual.
            try:
                answer = resp.json().get("answer", resp.text)
            except Exception:
                answer = resp.text
        except Exception as e:
            answer = f"ERROR: {e}"
        save_result(qid, answer)
        print(f"[{qid}] Pregunta: {qtext}")
        print(f"   Esperada: {expected}")
        print(f"   Respondida: {answer}")
        print("----")

    print("✅ Test finalizado. Resultados guardados en agent_test_results.")

if __name__ == "__main__":
    main()
