import pytest
import datahelper.playplatform as play_platform_helper


class TestCloudPlatform:

    @pytest.mark.daily
    def test_get_arrangements(self):
        # get all arrangements info
        arrangements = play_platform_helper.get_arrangements(None, None)
        print(arrangements)
