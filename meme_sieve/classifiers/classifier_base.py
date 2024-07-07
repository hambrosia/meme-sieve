from abc import ABC, abstractmethod


class ClassifierBase(ABC):

    @abstractmethod
    def generate_text_using_image(
            self,
            prompt:     str | None, 
            image_path: str | None, 
            model_name: str | None, 
            sleep_time: int=4):
        pass
