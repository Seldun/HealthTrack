import json
from datetime import datetime
import requests


class HealthAdvisorAI:
    def __init__(self, user_data):
        self.user_data = user_data
        self.advice = []
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
        self.headers = {"Authorization": "Bearer your_key"}

    def _generate_prompt(self):
        age = self.calculate_age()
        bmi = self.calculate_bmi()

        return f"""
        [INST] Вы - опытный врач-терапевт. Дайте рекомендации пациенту:
        Имя: {self.user_data['window1']['name']}
        Возраст: {age}
        Пол: {self.user_data['window1']['gender']}
        Рост: {self.user_data['window2']['height']} см
        Вес: {self.user_data['window2']['weight']} кг
        Национальность: {self.user_data["window2"]["nationality"]}
        Симптомы: {self.user_data['window3']}

        Составьте:
        1. 3 возможных диагноза (вероятность в %)
        2. Рекомендуемые безрецептурные лекарства
        3. Упражнения/процедуры
        4. Рекомендации по образу жизни
        Ответ оформляй маркированным списком на русском языке и пояснение в скобках на латыне только для названия болезни. Сам ответ и рекомедачии должны быть строго на русском языке  [/INST]
        """

    def query_ai(self, max_tokens=600):
        try:
            prompt = self._generate_prompt()
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json={"inputs": prompt, "parameters": {"max_new_tokens": max_tokens}}
            )

            # Проверка статуса ответа
            if response.status_code != 200:
                return f"Ошибка API: {response.status_code} - {response.text}"

            response_data = response.json()

            # Обработка разных форматов ответа
            if isinstance(response_data, list):
                generated_text = response_data[0].get('generated_text', 'Не удалось получить ответ')
            elif isinstance(response_data, dict):
                if 'error' in response_data:
                    return f"Ошибка модели: {response_data['error']}"
                generated_text = response_data.get('generated_text', 'Ответ не содержит данных')
            else:
                return "Неизвестный формат ответа"

            # Проверка на обрезанный ответ
            if generated_text.strip().endswith("...") or generated_text.strip().endswith(".."):
                # Если ответ обрезан, повторяем запрос с увеличенным лимитом токенов
                return self.query_ai(max_tokens=max_tokens + 200)
            return generated_text

        except Exception as e:
            return f"Ошибка при запросе: {str(e)}"

    def calculate_age(self):
        birthday = datetime.strptime(self.user_data['window1']['birthday'], "%Y-%m-%d")
        return datetime.today().year - birthday.year

    def calculate_bmi(self):
        height_m = self.user_data['window2']['height'] / 100
        return round(self.user_data['window2']['weight'] / (height_m ** 2), 1)

    def generate_full_report(self):
        # Базовые рекомендации
        self.advice.append(f" Персональный медицинский отчет для {self.user_data['window1']['name']}:")
        self.advice.append(f" Возраст: {self.calculate_age()} лет | ИМТ: {self.calculate_bmi()}")

        # AI рекомендации
        ai_response = self.query_ai()
        if '[/INST]' in ai_response:
            ai_response = ai_response.split('[/INST]')[-1].strip()
        self.advice.append("\n AI-рекомендации:\n" + ai_response)

        # Важные предупреждения
        self.advice.append("\n Важно: Данные рекомендации не заменяют консультацию врача!")
        with open("answer.txt", "w", encoding="utf-8") as s:
            s.write("\n".join(self.advice))
            print("health track")
        return "\n".join(self.advice)


# Пример использования
if __name__ == "__main__":
    input_data = {
        "window1": {
            "name": "Петров Михаил Григорьевич",
            "gender": "male",
            "birthday": "2008-01-01"
        },
        "window2": {
            "height": 181,
            "weight": 71,
            "nationality": "Голубые",
            "hair_color": "Брюнет"
        },
        "window3": {
            "symptoms": "Сыпь, аллергия, похмелье",
            "throat": "throat_issue",
            "stomach": "stomach_issue",
            "temperature": "temperature_issue"
        }
    }

    # Создаем экземпляр советника
    advisor = HealthAdvisorAI(input_data)

    # Генерируем и выводим отчет
    print(advisor.generate_full_report())
