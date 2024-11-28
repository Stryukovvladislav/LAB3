import requests
import json

VK_API_VERSION = "5.131"

def get_user_info(user_id, access_token):
    """Получить информацию о пользователе."""
    url = "https://api.vk.com/method/users.get"
    params = {
        "user_ids": user_id,
        "fields": "city,followers_count",
        "access_token": access_token,
        "v": VK_API_VERSION
    }
    response = requests.get(url, params=params).json()
    if "error" in response:
        print(f"Ошибка при получении информации о пользователе: {response['error']['error_msg']}")
        return {}
    return response

def get_user_names(user_ids, access_token):
    """Получить имена пользователей по их ID."""
    url = "https://api.vk.com/method/users.get"
    params = {
        "user_ids": ",".join(map(str, user_ids)),
        "access_token": access_token,
        "v": VK_API_VERSION
    }
    response = requests.get(url, params=params).json()
    if "response" in response:
        return [{"id": user["id"], "name": f"{user['first_name']} {user['last_name']}"} for user in response["response"]]
    return []

def get_followers(user_id, access_token):
    """Получить список подписчиков пользователя с их именами."""
    url = "https://api.vk.com/method/users.getFollowers"
    params = {
        "user_id": user_id,
        "count": 1000,
        "access_token": access_token,
        "v": VK_API_VERSION
    }
    response = requests.get(url, params=params).json()
    if "response" in response:
        follower_ids = response["response"].get("items", [])
        # Преобразуем ID в имена
        return get_user_names(follower_ids, access_token)
    else:
        print(f"Ошибка при получении подписчиков: {response.get('error', {}).get('error_msg', 'Неизвестная ошибка')}")
        return []

def get_subscriptions(user_id, access_token):
    """Получить список подписок пользователя с их именами."""
    url = "https://api.vk.com/method/users.getSubscriptions"
    params = {
        "user_id": user_id,
        "count": 1000,
        "access_token": access_token,
        "v": VK_API_VERSION
    }
    response = requests.get(url, params=params).json()
    subscription_ids = response.get("response", {}).get("users", [])
    return get_user_names(subscription_ids, access_token)

def get_groups(user_id, access_token):
    """Получить список групп пользователя с их названиями."""
    url = "https://api.vk.com/method/groups.get"
    params = {
        "user_id": user_id,
        "extended": 1,  # Запрашиваем детальную информацию о группах
        "fields": "name",
        "count": 100,
        "access_token": access_token,
        "v": VK_API_VERSION
    }
    response = requests.get(url, params=params).json()
    groups = response.get("response", {}).get("items", [])
    return [{"id": group["id"], "name": group["name"]} for group in groups]

def fetch_vk_data(user_id, access_token):
    """Собрать все данные о пользователе VK."""
    print("Получение данных пользователя...")
    user_info = get_user_info(user_id, access_token)

    print("Получение подписчиков...")
    followers = get_followers(user_id, access_token)

    print("Получение подписок...")
    subscriptions = get_subscriptions(user_id, access_token)

    print("Получение групп...")
    groups = get_groups(user_id, access_token)

    # Формирование итоговой структуры
    data = {
        "user_info": user_info.get("response", [{}])[0],
        "followers": followers,
        "subscriptions": subscriptions,
        "groups": groups
    }

    # Сохранение в JSON файл
    with open("vk_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print("Данные сохранены в 'vk_data.json'.")

if __name__ == "__main__":
    print("Введите ваш токен доступа VK.")
    access_token = input("Токен: ").strip()
    
    if not access_token:
        print("Токен не введён. Завершение работы.")
    else:
        user_id = input("Введите ID пользователя VK (например, свой): ").strip()
        fetch_vk_data(user_id, access_token)