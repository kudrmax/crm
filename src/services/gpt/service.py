from __future__ import annotations

import dataclasses
from typing import List, Any, Tuple

from src.models.log.models import MLog

from yandex_cloud_ml_sdk import YCloudML

from src.services.gpt import config


@dataclasses.dataclass
class GPTResult:
    input: Any
    output: str


class GPTService:
    def __init__(self):
        self.sdk = YCloudML(
            folder_id=config.folder_id,
            auth=config.api_key,
        )

    def _create_request(self, messages) -> GPTResult:
        result = self.sdk.models.completions("yandexgpt").configure(temperature=0.5).run(messages)

        text = result.alternatives[0].text

        return GPTResult(
            output=str(text),
            input=messages,
        )

    def _get_bullet_list_from_text(self, text: str) -> Tuple[str, GPTResult]:
        messages = [
            {
                "role": "system",
                "text":
                    """
                    Преобразуй следующий текст в структурированный bullet список фактов о человеке.
                    Факты должны быть краткими, без лишних вводных слов, но содержательными.
                    Если в тексте есть важные акценты (например, что-то показалось важным собеседнику), отмечай их знаком "!" перед фактом.
                    
                    Формат ответа:
                    - [Краткий факт]
                    - ! [Факт, который имеет особое значение]
                    - [Краткий факт]
                    
                    Если в тексте упоминаются другие люди или цифры (зарплаты, даты), сохрани их точность. 
                    Если факт содержит личное мнение человека, отметь это явно (например, "Считает, что ...").
                    """,
            },
            {
                "role": "user",
                "text": text,
            },
        ]
        gpt_result = self._create_request(messages)
        return gpt_result.output, gpt_result

    def _get_logs_from_bullet_list(self, text: str) -> List[MLog]:
        pass

    def get_logs_from_text(self, text: str) -> List[MLog]:
        bullet_list, _ = self._get_bullet_list_from_text(text)
        return self._get_logs_from_bullet_list(bullet_list)


gpt_service = GPTService()

# text, result = s.convert_text_to_bullet_logs("""
# Марко училась в Питере на программе, где сам создаёшь программу, и у неё направление в итоге было связано с когнитивистикой. Диплом написала, используя нейросети Torch, когнитивистику, суть была в том, что инцефалограммы или что-то такое сравнивало использование каких-то обычных нейронных сетей и графовых, у которых есть трейсинг. И вывод, трейсинг важен.
# """)
# print(text)
# print(result)

# text, result = s.convert_text_to_bullet_logs("""
# Сейчас учится в школе 21 на направлении Data Science. Рассказала мне о том, что у неё есть знакомый, который работает во ВИТа на ГО с зарплатой 800 тысяч. Ещё рассказала, что... Неважно.""")
# print(text)
# print(result)
