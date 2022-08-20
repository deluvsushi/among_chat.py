import requests
from os import urandom
from hashlib import md5

class AmongChat:
	def __init__(
			self,
			app_version: str = "2.2.1-220630311",
			app_identifier: str = "walkie.talkie.among.us.friends",
			device_type: str = "android",
			language: str = "ru",
			model: str = "SM-G9880",
			brand: str = "samsung",
			country_code: str = "RU",
			push_type: str = "FCM"):
		self.api = "https://api.among.chat"
		self.headers = {
			"user-agent": "okhttp/4.4.0",
			"connection": "Keep-Alive"}
		self.user_id = None
		self.access_token = None
		self.language = language
		self.push_type = push_type
		self.device_type = device_type
		self.app_version = app_version
		self.country_code = country_code
		self.app_identifier = app_identifier
		self.device_id = self.generate_device_id()
		self.android_id = self.generate_android_id()
		self.headers["x-among-ua"] = f"appVersion={self.app_version};appIdentifier={self.app_identifier};deviceType={self.device_type};deviceId={self.device_id};lang={self.language};androidId={self.android_id};countryCode={self.country_code};pushType={self.push_type};"

	def generate_device_id(self):
		return md5(urandom(15)).hexdigest()

	def generate_android_id(self):
		return md5(urandom(10)).hexdigest()[:16]

	def login(
			self,
			provider: str = "device",
			client_type: str = "android",
			box_token: int = 1):
		data = {
			"provider": provider,
			"client_type": client_type,
			"box_token": box_token
		}
		response = requests.post(
			f"{self.api}/auth/login",
			json=data,
			headers=self.headers).json()
		if "access_token" in response["data"]:
			self.user_id = response["data"]["uid"]
			self.access_token = response["data"]["access_token"]
			self.headers["x-uid"] = f"{self.user_id}"
			self.headers["x-access-token"] = self.access_token
			self.headers["x-among-ua"] += "uid={self.user_id};"
		return response
			
	def login_with_google(
			self,
			google_id_token: str,
			client_type: str = "android",
			box_token: int = 1):
		data = {
			"token": google_id_token,
			"provider": "google",
			"client_type": client_type,
			"box_token": box_token
		}
		return requests.post(
			f"{self.api}/auth/login",
			json=data,
			headers=self.headers).json()

	def edit_profile(
			self,
			nickname: str = None,
			description: str = None,
			hide_location: bool = True,
			birthday: str = "19880101"):
		data = {
			"profile_data": {
				"birthday": birthday
			}
		}
		if nickname:
			data["profile_data"]["name"] = nickname
		if description:
			data["profile_data"]["description"] = description
		if hide_location:
			data["profile_data"]["hide_location"] = hide_location
		return requests.post(
			f"{self.api}/account/profile",
			json=data,
			headers=self.headers).json()

	def get_account_profile(self):
		return requests.get(
			f"{self.api}/account/profile",
			headers=self.headers).json()

	def get_setting(self):
		return requests.get(
			f"{self.api}/api/v1/setting",
			headers=self.headers).json()

	def get_banned_keywords(self):
		return requests.get(
			f"{self.api}/live/keyword/blacklist",
			headers=self.headers).json()

	def get_finance_info(self):
		return requests.get(
			f"{self.api}/finance/info",
			headers=self.headers).json()

	def get_summary(self):
		return requests.get(
			f"{self.api}/api/v1/summary",
			headers=self.headers).json()

	def get_rooms_list(self):
		return requests.get(
			f"{self.api}/api/v1/trend/list",
			headers=self.headers).json()

	def get_account_pets(self):
		return requests.get(
			f"{self.api}/account/my/pet/list",
			headers=self.headers).json()

	def get_topics(self):
		return requests.get(
			f"{self.api}/api/v1/topics/v2",
			headers=self.headers).json()

	def get_group_list(
			self,
			skip: int = 0,
			limit: int = 20):
		return requests.get(
			f"{self.api}/api/v1/group/list?skip={skip}&limit={limit}",
			headers=self.headers).json()

	def get_agora_live_token(self):
		return requests.get(
			f"{self.api}/live/token/agora",
			headers=self.headers).json()

	def get_room_info(self, room_id: str):
		return requests.get(
			f"{self.api}/api/v1/rooms/room?room_id={room_id}",
			headers=self.headers).json()

	def get_room_live_token(self, room_id: str):
		return requests.get(
			f"{self.api}/live/room/token?room_id={room_id}",
			headers=self.headers).json()

	def join_room(
			self,
			room_id: str,
			code: str = None,
			source: str = "join_friend_room",
			rtc_support: str = "agora,zego",
			with_full_recommend: int = 1):
		url = f"{self.api}/api/v1/rooms/enter?room_id={room_id}&source={source}&rtc_support={rtc_support}&with_full_recommend={with_full_recommend}"
		if code:
			url += f"&code={code}"
		return requests.get(url, headers=self.headers).json()

	def leave_room(self, room_id: str):
		return requests.get(
			f"{self.api}/api/v1/rooms/leave?room_id={room_id}",
			headers=self.headers).json()

	def get_pet_info(self, pet_id: int):
		return requests.get(
			f"{self.api}/account/pet/info?upid={pet_id}",
			headers=self.headers).json()

	# work - 0 = end working
	# work - 1 = start working
	def pet_work(self, pet_id: int, work: int = 1):
		data = {
			"work": work,
			"upid": pet_id
		}
		return requests.post(
			f"{self.api}/account/pet/work",
			json=data,
			headers=self.headers).json()

	def get_user_status(self, user_id: int):
		return requests.get(
			f"{self.api}/api/v1/user/status?uid={user_id}",
			headers=self.headers).json()

	def get_report_reasons(self):
		return requests.get(
			f"{self.api}/live/report/reason",
			headers=self.headers).json()

	def block_user(self, user_id: int):
		return requests.put(
			f"{self.api}/social/relation?target_uid={user_id}&relation_type=block",
			headers=self.headers).json()

	def unblock_user(self, user_id: int):
		return requests.delete(
			f"{self.api}/social/relation?target_uid={user_id}&relation_type=block",
			headers=self.headers).json()

	def follow_user(self, user_id: int):
		return requests.put(
			f"{self.api}/social/relation?target_uid={user_id}&relation_type=follow",
			headers=self.headers).json()

	def unfollow_user(self, user_id: int):
		return requests.delete(
			f"{self.api}/social/relation?target_uid={user_id}&relation_type=follow",
			headers=self.headers).json()

	def get_user_profile(
			self,
			user_id: int,
			with_tabs: int = 1,
			show_unique: int = 1):
		return requests.get(
			f"{self.api}/account/profile/page?uid={user_id}&with_tabs={with_tabs}&show_unique={show_unique}",
			headers=self.headers).json()

	def get_user_relation(self, user_id: int):
		return requests.get(
			f"{self.api}/account/profile/relation?uid={user_id}",
			headers=self.headers).json()

	def get_account_groups(
			self,
			skip: int = 0,
			limit: int = 20):
		return requests.get(
			f"{self.api}/api/v1/my/group/list?skip={skip}&limit={limit}",
			headers=self.headers).json()

	def apply_group(self, group_id: str):
		data = {"gid": group_id}
		return requests.post(
			f"{self.api}/api/v1/group/apply",
			json=data,
			headers=self.headers).json()

	def get_group_info(self, group_id: str):
		return requests.get(
			f"{self.api}/api/v1/group?gid={group_id}",
			headers=self.headers).json()

	def join_group(self, group_id: str):
		return requests.get(
			f"{self.api}/api/v1/group/live/enter?gid={group_id}",
			headers=self.headers).json()

	def leave_group(self, group_id: str):
		return requests.get(
			f"{self.api}/api/v1/group/live/leave?gid={group_id}",
			headers=self.headers).json()

	def get_group_live_users(
			self,
			group_id: str,
			exclude_user_ids: str = "",
			limit: int = 20):
		data = {
			"exclude_uids": exclude_user_ids,
			"gid": group_id,
			"limit": limit
		}
		return requests.post(
			f"{self.api}/api/v1/group/live/user/list",
			json=data,
			headers=self.headers).json()

	def get_group_users(
			self,
			group_id: str,
			limit: int = 20):
		return requests.get(
			f"{self.api}/api/v1/group/member/list?gid={group_id}&limit={limit}",
			headers=self.headers).json()

	def get_online_strangers(self):
		return requests.get(
			f"{self.api}/api/v1/online/stranger/list",
			headers=self.headers).json()

	def invite_to_room(
			self,
			room_id: str,
			user_id: int,
			is_stranger: int = 1):
		data = {
			"is_stranger": is_stranger,
			"uid": user_id,
			"room_id": room_id
		}
		return requests.post(
			f"{self.api}/api/v1/rooms/invite",
			json=data,
			headers=self.headers).json()

	def get_user_followers(
			self,
			user_id: int,
			limit: int = 20,
			skip: int = 0):
		return requests.get(
			f"{self.api}/social/relation/followers?uid={user_id}&limit={limit}&skip_ms={skip}",
			headers=self.headers).json()

	def get_user_followings(
			self,
			user_id: int,
			limit: int = 20,
			skip: int = 0):
		return requests.get(
			f"{self.api}/social/relation?uid={user_id}&relation_type=follow&limit={limit}&skip_ms={skip}",
			headers=self.headers).json()

	def level_up_pet(self, pet_id: int):
		data = {"upid": pet_id}
		return requests.post(
			f"{self.api}/account/pet/level/up",
			json=data,
			headers=self.headers).json()

	def get_diamond_products(self):
		return requests.get(
			f"{self.api}/finance/diamond/products",
			headers=self.headers).json()

	def get_egg_products(self):
		return requests.get(
			f"{self.api}/finance/egg/products",
			headers=self.headers).json()

	def get_pet_atlas(self):
		return requests.get(
			f"{self.api}/account/pet/atlas",
			headers=self.headers).json()

	def buy_pet(self):
		return requests.post(
			f"{self.api}/account/coin/pet/buy",
			data={},
			headers=self.headers).json()

	def get_blocked_users(
			self,
			limit: int = 20,
			skip: int = 0):
		return requests.get(
			f"{self.api}/social/relation?uid={self.user_id}&relation_type=block&limit={limit}&skip_ms={skip}",
			headers=self.headers).json()
