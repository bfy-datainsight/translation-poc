import yaml
from src.support import quoted, quoted_presenter

yaml.add_representer(quoted, quoted_presenter)
from typing import Optional

from src.worksheet.writer.wrappers import WorkSheetWriter
from src.worksheet.reader.wrappers import WorkSheetReader
from src.configuration.configuration import Configuration
from src.library.library import Library

configuration = Configuration()
library = Library().from_file(path="content\library\output.yml")


def main(source_path: str) -> None:
    source_worksheet = WorkSheetReader().read(path=source_path)
    worksheets: Optional[list] = configuration.worksheets
    assert worksheets, "No worksheet found in the configuration file"

    for worksheet in worksheets:
        name: str = worksheet["name"]
        target_locale: str = worksheet["locale"]
        guid: str = worksheet["uuid"]

        WorkSheetWriter(
            full_worksheet=source_worksheet, name=name, library=library
        ).transform(guid=guid, target_locale=target_locale).write(
            output_dir="content/output"
        )
    return None


if __name__ == "__main__":
    main(source_path="content\input\Search Orders.worksheet.tml")
