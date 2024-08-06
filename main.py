import json
import requests
import bs4
from fake_headers import Headers


def get_headers():
    return Headers(os="win", browser="chrome").generate()

response = requests.get("https://spb.hh.ru/search/vacancy?text=python&area=1&area=2", headers=get_headers())
soup = bs4.BeautifulSoup(response.text, features="lxml")
soups= soup.find("div", {"data-qa" :"vacancy-serp__results"})
hh_soups = soups.find_all("div", {"data-sentry-element": "Element"})

vacancies = []
for hh_soup in hh_soups:
    link = hh_soup.find("a",{"target" :"_blank" })["href"]

    if link:
        response = requests.get(link, headers=get_headers())
        vacancy = bs4.BeautifulSoup(response.text, features="lxml")
        vacancy_description = vacancy.find("div", class_="g-user-content" )
        vacancy_description_text = " ".join(vacancy_description.text.split()).lower()

        if ("django" or "flask") in vacancy_description_text:
            city = hh_soup.find("span", {"data-qa" : "vacancy-serp__vacancy-address"})
            name = hh_soup.find("span", class_= "vacancy-name--c1Lay3KouCl7XasYakLk serp-item__title-link")
            company = hh_soup.find("span", class_="company-info-text--vgvZouLtf8jwBmaD1xgp" )
            salary = hh_soup.find("span", class_="fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni compensation-text--kTJ0_rp54B2vNeZ3CTt2 separate-line-on-xs--mtby5gO4J0ixtqzW38wh")
            if salary == None:
                salary = "зарплата не указана"
            else:
                salary = salary.text
            
            vacancy_data = {
                "вакансия": name.text,
                "ссылка": link,
                "зп": salary,
                "название компании": company.text,
                "город": city.text
            }
            vacancies.append(vacancy_data)


with open("vacancies.json", "w", encoding="utf-8") as f:
    json.dump(vacancies, f, ensure_ascii=False, indent=5)