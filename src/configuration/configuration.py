from typing import Optional
import yaml


class Configuration:
    def __init__(self, path: str = "src\configuration\config.yml"):
        self = self
        with open(path, encoding="utf8") as file:
            configuration: dict = yaml.safe_load(file)
        self.worksheets: Optional[list[dict]] = configuration.get("worksheets")
        assert self.worksheets
        self.liveboards: Optional[list[dict]] = configuration.get("liveboards")
        assert self.liveboards

    def get_worksheet_name(self, uuid: str) -> str:
        """Fix generic mapping function for this"""
        worksheet: Optional[dict[str, str]] = [
            ws for ws in self.worksheets if ws.get("uuid") == uuid
        ][0]
        assert worksheet
        return worksheet["name"]

    def get_worksheet_uuid(self, name: str) -> str:
        worksheet: Optional[dict[str, str]] = [
            ws for ws in self.worksheets if ws.get("name") == name
        ][0]
        assert worksheet
        return worksheet["uuid"]
