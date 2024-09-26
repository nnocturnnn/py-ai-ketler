import os
from io import BytesIO

import instaloader
import requests
from openai import OpenAI

client = OpenAI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INSTAGRAM_PROFILE = os.getenv("INSTAGRAM_PROFILE")
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")


def login_instagram() -> instaloader.Instaloader:
    """
    Авторизація в Instagram через Instaloader.
    :return: Об'єкт Instaloader з авторизованою сесією.
    """
    loader = instaloader.Instaloader()

    try:
        loader.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        return loader
    except instaloader.exceptions.BadCredentialsException:
        raise ValueError("Неправильне ім'я користувача або пароль.")
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        raise RuntimeError("Необхідна двофакторна автентифікація. Використовуйте її.")
    except Exception as e:
        raise RuntimeError(f"Помилка при авторизації в Instagram: {str(e)}")


def get_instagram_profile(loader: instaloader.Instaloader, profile_username: str):
    """
    Парсинг профілю Instagram, отримання фото профілю, опису та останніх постів.
    :param loader: Авторизований Instaloader.
    :param profile_username: Instagram ім'я профілю.
    :return: Дані профілю - фото, опис, пости.
    """
    try:
        profile = instaloader.Profile.from_username(loader.context, profile_username)
        profile_data = {
            "username": profile_username,
            "full_name": profile.full_name,
            "bio": profile.biography,
            "profile_pic_url": profile.profile_pic_url,
            "posts": [],
        }

        for post in profile.get_posts():
            if len(profile_data["posts"]) >= 5:
                break
            post_data = {
                "caption": post.caption or "No Caption",
                "image_url": post.url if post.is_video is False else None,
                "is_video": post.is_video,
            }
            profile_data["posts"].append(post_data)

        return profile_data
    except instaloader.exceptions.ProfileNotExistsException:
        raise ValueError(f"Профіль '{profile_username}' не існує.")
    except Exception as e:
        raise RuntimeError(f"Помилка при отриманні профілю Instagram: {str(e)}")


def fetch_image_data(image_url: str) -> BytesIO:
    """
    Отримання даних зображення за наданим URL.
    :param image_url: URL зображення.
    :return: Дані зображення у вигляді BytesIO.
    """
    response = requests.get(image_url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        raise RuntimeError(f"Не вдалося отримати зображення з {image_url}")


def analyze_content_with_openai(bio: str, posts: list) -> str:
    """
    Аналіз біографії та постів профілю за допомогою OpenAI GPT і створення повідомлення.
    :param bio: Біографія профілю.
    :param posts: Список постів профілю.
    :return: Сформоване повідомлення.
    """
    post_descriptions = "\n".join([f"Пост: {post['caption']}" for post in posts])
    prompt = (
        f"Біографія: {bio}\n"
        f"Ось останні пости:\n{post_descriptions}\n"
        "Створи дружнє повідомлення, щоб познайомитися з цією людиною на основі її профілю."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Ти помічник, що створює дружні повідомлення.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return response.choices[0].message.content.strip()


def create_greeting_message(profile_data: dict) -> str:
    """
    Створює привітальне повідомлення на основі даних профілю Instagram.
    :param profile_data: Дані профілю Instagram (біографія, фото, пости).
    :return: Генероване повідомлення.
    """
    bio = profile_data.get("bio", "Немає біографії")
    posts = profile_data.get("posts", [])
    return analyze_content_with_openai(bio, posts)


def main():
    try:
        loader = login_instagram()
        insta_profile = input("Введіть ім'я профілю Instagram: ")
        profile_data = get_instagram_profile(loader, insta_profile)

        message = create_greeting_message(profile_data)
        print(f"Згенероване повідомлення: {message}")

    except Exception as e:
        print(f"Помилка: {str(e)}")


if __name__ == "__main__":
    main()
