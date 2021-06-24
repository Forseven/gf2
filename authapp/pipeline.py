from collections import OrderedDict
from datetime import datetime
from tempfile import NamedTemporaryFile
from urllib.parse import urlencode, urlunparse
from urllib.request import urlopen

import requests
from django.core.files import File
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about','photo_200')),
                                                access_token=response['access_token'],
                                                v='5.92')),None
                          ))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    #get avatar

    if data['photo_200']:

        # Save avatar
        image_url = data['photo_200']
        avatar_temp = NamedTemporaryFile(delete=True)
        avatar_temp.write(urlopen(image_url).read())
        avatar_temp.flush()

        user.avatar.save("image_%s" % user.pk, File(avatar_temp))
        user.save()

    if data['sex']:
        user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

    if data['about']:
        user.shopuserprofile.aboutMe = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    user.save()
