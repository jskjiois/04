"""
Практическое занятие №4
Отправка запросов к LLM API на Python (GigaChat)

Схема работы:
Пользователь -> Python -> LLM API -> Большая языковая модель -> Ответ пользователю
"""

from dotenv import load_dotenv
import os
from gigachat import GigaChat

# --- Загружаем ключ из файла .env ---
load_dotenv()
key = os.getenv("GIGACHAT_CREDENTIALS")


def ask_llm(prompt: str) -> str:
    """
    Отправляет prompt в GigaChat и возвращает текст ответа.
    Позволяет обращаться к модели многократно из разных мест программы.
    """
    if not key:
        raise ValueError(
            "API-ключ не найден. Проверьте, что файл .env существует "
            "и содержит переменную GIGACHAT_CREDENTIALS."
        )

    with GigaChat(
        credentials=key,
        model="GigaChat-2",
        verify_ssl_certs=False,
    ) as client:
        response = client.chat(prompt)
        return response.choices[0].message.content


def show_menu() -> None:
    """Мини-проект: меню для общения с ИИ-помощником."""
    menu_text = (
        "\nИИ-помощник студента\n"
        "1 — объяснить тему\n"
        "2 — придумать идеи\n"
        "3 — составить план\n"
        "0 — выход\n"
    )

    prompts = {
        "1": "Объясни студенту простыми словами тему: ",
        "2": "Придумай несколько идей на тему: ",
        "3": "Составь пошаговый план по теме: ",
    }

    while True:
        print(menu_text)
        choice = input("Выберите пункт меню: ").strip()

        if choice == "0":
            print("Выход из программы.")
            break

        if choice not in prompts:
            print("Неверный пункт меню, попробуйте снова.")
            continue

        topic = input("Введите тему: ").strip()
        full_prompt = prompts[choice] + topic

        try:
            answer = ask_llm(full_prompt)
            print("\nОтвет модели:\n" + answer)
        except Exception as error:
            print("Ошибка:", error)


if __name__ == "__main__":
    show_menu()