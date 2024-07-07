from abc import ABC, abstractmethod


class ClassifierBase(ABC):

    @abstractmethod
    def generate_text_using_image(
            self,
            prompt:         str | None, 
            image_path:     str | None, 
            model_name:     str | None, 
            model_version:  str | None,
            sleep_time:     int | None
            ):
        pass
