from langchain.output_parsers import PydanticOutputParser
from src.llm.groq_client import get_groq_llm
from src.prompts.templates import mcq_prompt_template, fill_blank_prompt_template
from src.config.settings import settings
from src.common.logger import get_logger
from src.common.custom_exception import CustomException
from src.models.questions_schemas import MCQQuestion, FillBlankQuestion

class QuestionGenerator():
    def __init__(self):
        self.llm = get_groq_llm()
        self.logger = get_logger(self.__class__.__name__)

    def _retry_and_parse(self, prompt, parser, topic, difficulty):
        for attempt in range(settings.max_retries):
            try:
                self.logger.info(f"Generating question for topic {topic} with difficulty {difficulty}")

                response = self.llm.invoke(prompt.format(topic=topic, difficulty=difficulty))

                parsed = parser.parse(response.content)
                
                self.logger.info("Successfully parsed the question")
                return parsed

            except Exception as e:
                self.logger.error(f"Error coming: {str(e)}")

                if attempt==settings.max_retries-1:
                    raise CustomException(f"Generation failed after {settings.max_retries} attempts", str(e))
                

    def generate_mcq(self, topic:str, difficulty:str='medium') -> MCQQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=MCQQuestion)
            question = self._retry_and_parse(mcq_prompt_template, parser, topic, difficulty)

            if len(question.options) != 4 or question.correct_answer not in question.options:
                raise ValueError("Invalid MCQ Structure")
            
            self.logger.info("Generated a Valid MCQ Question")

            return question
        
        except Exception as e:
            self.logger.error("Failed to generate MCQ ", str(e))
            raise CustomException("MCQ Generation failed", e)
        
    def generate_fill_blank(self, topic:str, difficulty:str='medium') -> FillBlankQuestion:
        try:
            parser = PydanticOutputParser(pydantic_object=FillBlankQuestion)
            question = self._retry_and_parse(fill_blank_prompt_template, parser, topic, difficulty)

            if "___" not in question.question:
                raise ValueError("Fill in blanks should contain '___'")
            
            self.logger.info("Generated a Valid Fill in Blank Question")

            return question
        
        except Exception as e:
            self.logger.error("Failed to generate Fill in blank Question ", str(e))
            raise CustomException("Fill in blank question Generation failed", e)
                    