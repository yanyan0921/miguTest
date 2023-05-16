from rest.playplatform.playplatform import PlayPlatformService

play_platform_service = PlayPlatformService()


def dict_ext(d1, d2):
    result = dict(d1)
    result.update(d2)
    return result


def get_arrangements(user_id, audience_id):
    return play_platform_service.get_arrangements(user_id, audience_id)
