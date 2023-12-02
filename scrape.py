from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time

# chrome_options = Options()

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

driver.get("http://www.neetcode.io/roadmap")
search_results = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "foreignObject"))
)

for topic in search_results:
    name = topic.text
    topic.click()

    questions = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tbody tr td a"))
    )
    wait.until(EC.visibility_of(questions[0]))
    question_links = []
    question_names = []
    for question in questions:
        if question.text == " ":
            question_links.pop()
            question_links.append(question.get_attribute("href"))
            continue
        question_links.append(question.get_attribute("href"))
        question_names.append(question.text)

    answers = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "tbody tr td div button fa-icon")
        )
    )

    answer_links = []
    for answer in answers:
        answer = answer.find_element(By.XPATH, "..")
        answer.click()
        app_modal = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, 'app-modal[width = "70%"]')
            )
        )

        answer_link = app_modal.find_element(By.CSS_SELECTOR, "h1 a")
        answer_links.append(answer_link.get_attribute("href"))

        close_button = app_modal.find_element(By.CSS_SELECTOR, "footer button")
        close_button.click()

    content = f"# **{name}**\n## **Questions**\n"
    for i, question_name in enumerate(question_names):
        content += f"{i + 1}. {question_name}\n\t[Question]({question_links[i]}) | [Answer]({answer_links[i]})\n"

    with open(f"DSA.md", "a") as f:
        f.write(content)

    escape = driver.find_element(
        By.CSS_SELECTOR, "app-graph app-sidebar div div button"
    )
    escape.click()
