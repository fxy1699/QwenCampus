import json
import random

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

base_url = "http://frp-add.com:18089/api/v1"
tokens_url_path = "/tokens"
albums_url_path = "/albums"
images_url_path = "/images"
upload_url_path = "/upload"
delete_url_path = "/images/"
auth = "2|t469zlqz2qCcwg1unDQ3sR9KrYLMMGAUBIFjmxO0"


class Lsky:
    def __init__(self):
        self.url = base_url
        self.token = ""

    def lsky_get_access(self, method='POST'):
        """
        获取tokens
        :return:
        """
        url = self.url + tokens_url_path
        data = {
            "email": "1003844689@qq.com",
            "password": "fxy162899"
        }
        headers = {
            "Accept": "application/json"
        }
        response = requests.post(url, data=data, headers=headers)
        # print(response.text)
        # print(type(response.text))
        self.token = json.loads(response.text)["data"]["token"]
        # print(self.token)
        # print(type(self.token))

    def lsky_get_albums(self, method='GET', order=None, keyword=None):
        """
        获取albums
        :param method:
        :param keyword:
        :param order:
        :return:
        """
        url = self.url + albums_url_path
        order = order if order is not None else []
        keyword = keyword if keyword is not None else []
        data = {
            "order": order,
            "keyword": keyword
        }
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer {}".format(auth)
        }
        response = requests.get(url, data=data, headers=headers)
        # print(response.text)
        albums = json.loads(response.text)["data"]["data"]
        # print(albums)
        return albums

    def lsky_get_images(self, auth=auth, album_id: int = 2, order="newest"):
        """
        获取图片
        :param auth:
        :param album_id:
        :param order:
        :return:
        """
        url = self.url + images_url_path
        params = {
            "order": order,
            "album_id": album_id,
            # "keyword": "",
        }
        headers = {
            "Accept": "application/json",
            # "Authorization": "Bearer {}".format(self.token),
            "Authorization": "Bearer {}".format(auth)
        }
        response = requests.get(url, params=params, headers=headers)
        # print(response.text)
        img_list = json.loads(response.text)["data"]["data"]
        print(img_list)
        # print(type(img_list))
        # for img in img_list:
        # 	if img["origin_name"] == "where-is-waldo.jpg":
        # 		print(img["links"]["url"])
        return img_list

    def lsky_upload_images(self, path, origin_name):
        """
        上传图片
        :param path:
        :return:
        """
        url = base_url + upload_url_path
        # file = {
        # 	'file': open(path, 'rb')
        # }
        file = open(path, 'rb')
        multipart_encoder = MultipartEncoder(
            fields={
                # 'file': ('test.jpg', img_file, "image/jpeg"),
                # "file": (str(origin_name), file, "image/png")
                "file": (str(origin_name), file, "image/jpeg")
            },
            # boundary = '-----------------------------' + str(random.randint(1e28, 1e29 - 1))
            boundary='----WebKitFormBoundaryJ2aGzfsg35YqeT7X'
        )
        headers = {
            "Accept": "application/json",
            'Content-Type': multipart_encoder.content_type,
            "Authorization": "Bearer {}".format(auth)
        }
        response = requests.post(url, data=multipart_encoder, headers=headers)
        json_response = json.loads(response.text)
        img_url = json_response["data"]["links"]["url"]
        key = json_response["data"]["key"]
        name = json_response["data"]["name"]
        origin_name = json_response["data"]["origin_name"]
        dict = {
            "url": img_url,
            "key": key,
            "name": name,
            "origin_name": origin_name
        }
        print(dict)
        return dict

    def lsky_delete_img(self, key):
        """
        删除图片
        :return:
        """
        url = base_url + delete_url_path + ":" + str(key)
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer {}".format(auth)
        }
        response = requests.delete(url=url, headers=headers)
        print(response.text)


if __name__ == '__main__':
    lsky = Lsky()
    # lsky.lsky_get_access()
    lsky.lsky_get_albums()
    lsky.lsky_get_images(album_id=2)
# 	dict = lsky.lsky_upload_images("../static/imgs/waldo.png")
# 	lsky.lsky_delete_img(key=dict["key"])

