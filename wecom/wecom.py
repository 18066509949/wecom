import requests


class WeChatWorkSender:
    def __init__(self, corpid, corpsecret, agentid):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self.access_token = self.get_access_token()

    def get_access_token(self):
        """
        获取企业微信的 access_token
        """
        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.corpid}&corpsecret={self.corpsecret}"
        response = requests.get(url)
        result = response.json()
        if 'access_token' in result:
            return result['access_token']
        else:
            raise Exception(f"Failed to get access token: {result}")

    def upload_media(self, media_type, media_path):
        """
        上传文件或图片，获取 media_id
        :param media_type: 媒体类型，如 'image' 或 'file'
        :param media_path: 媒体文件的本地路径
        """
        url = f"https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={self.access_token}&type={media_type}"
        files = {'media': open(media_path, 'rb')}
        response = requests.post(url, files=files)
        result = response.json()
        if 'media_id' in result:
            return result['media_id']
        else:
            raise Exception(f"Failed to upload media: {result}")

    def send_text(self, user_ids, content):
        """
        发送文本消息
        :param user_ids: 接收消息的用户 ID 列表
        :param content: 消息内容
        """
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}"
        data = {
            "touser": "|".join(user_ids),
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": content
            }
        }
        response = requests.post(url, json=data)
        return response.json()

    def send_image(self, user_ids, image_path):
        """
        发送图片消息
        :param user_ids: 接收消息的用户 ID 列表
        :param image_path: 图片文件的本地路径
        """
        media_id = self.upload_media('image', image_path)
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}"
        data = {
            "touser": "|".join(user_ids),
            "msgtype": "image",
            "agentid": self.agentid,
            "image": {
                "media_id": media_id
            }
        }
        response = requests.post(url, json=data)
        return response.json()

    def send_file(self, user_ids, file_path):
        """
        发送文件消息
        :param user_ids: 接收消息的用户 ID 列表
        :param file_path: 文件的本地路径
        """
        media_id = self.upload_media('file', file_path)
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={self.access_token}"
        data = {
            "touser": "|".join(user_ids),
            "msgtype": "file",
            "agentid": self.agentid,
            "file": {
                "media_id": media_id
            }
        }
        response = requests.post(url, json=data)
        return response.json()


# 发送企业微信消息
def uxin_wx(name, message):
    corpid = "wxd4e113eb4c0136b9"
    corpsecret = "PMfPOv2Qqq0iXZAdWHF7WdaW4kkWUZcwyGE4NZtve3k"
    agentid = "1000026"
    sender = WeChatWorkSender(corpid, corpsecret, agentid)
    try:
        if isinstance(message, str):  # 判断是否为文本消息
            result = sender.send_text([name], message)
        elif isinstance(message, str) and message.endswith(('.jpg', '.jpeg', '.png', '.gif')):  # 判断是否为图片消息
            result = sender.send_image([name], message)
        elif isinstance(message, str) and message.endswith(('.xlsx', '.docx', '.pdf', '.txt')):  # 判断是否为文件消息
            result = sender.send_file([name], message)
        else:
            print("不支持的消息类型")
            return
        if result.get('errcode') == 0:  # 判断发送是否成功
            print(f"给 {name} 的消息发送成功")
        else:
            print(f"给 {name} 的消息发送失败，错误码：{result.get('errcode')}，错误信息：{result.get('errmsg')}")
    except Exception as e:
        print(f"发送失败，报错信息: {e}")
