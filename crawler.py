import requests
import requests.auth

# Conseguir el token de acceso
client_auth = requests.auth.HTTPBasicAuth('PA80r16sX4tHy6rnYkpdyw', 'Tsw4ky4M2gp3l0pEbD61a2q0fOTwZQ')
post_data = {"grant_type": "password", "username": "moy--", "password": "c53a8c7549"}
headers = {"User-Agent": "crawler-ar by moy--"}

token = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)


# Usar el token para acceder
headers["Authorization"] = "bearer " + token.json().get('access_token')

# Ej:
# response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)

# print(response.json().get('comment_karma'))
